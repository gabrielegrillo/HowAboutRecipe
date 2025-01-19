import os

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.core.files.uploadedfile import SimpleUploadedFile

from HowAboutRecipe import settings
from recipes.models import Recipe, Ingredient, Tag, RecipeIngredients, Rating, Comment, RecipeImage
from io import BytesIO
from PIL import Image
from users.models import User
from recipes.serializers import (
    RecipeSerializer,
    RecipeIngredientsSerializer,
    IngredientSerializer,
    TagSerializer,
    RatingSerializer, CommentSerializer, RecipeImageSerializer,
)


class SerializerTestCase(TestCase):
    def setUp(self):
        # Setup iniziale per i test
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()

        # Genera un token JWT per l'utente
        self.token = str(AccessToken.for_user(self.user))

        self.tag1 = Tag.objects.create(name="Vegan")
        self.tag2 = Tag.objects.create(name="Gluten-Free")
        self.ingredient1 = Ingredient.objects.create(name="Sugar")
        self.ingredient2 = Ingredient.objects.create(name="Flour")
        self.recipe = Recipe.objects.create(
            title="Chocolate Cake",
            description="Delicious chocolate cake",
            author=self.user,
            preparation_time=60,
            difficulty=4,
            steps="1.a\n2.b\n3.c\n4.d\n5.e\n6.f",
            is_public=False,
        )

        self.recipe_ingredient1 = RecipeIngredients.objects.create(
            recipe=self.recipe, ingredient=self.ingredient1, quantity=3, unit="A"
        )
        self.recipe_ingredient2 = RecipeIngredients.objects.create(
            recipe=self.recipe, ingredient=self.ingredient2, quantity=1, unit="m"
        )



        self.rating = Rating.objects.create(author=self.user, recipe=self.recipe, rating=5)
        self.second_user = User.objects.create_user(username="testuser2", password="pwd")
        self.rating2 = Rating.objects.create(author=self.second_user, recipe=self.recipe, rating=3)

        self.comment1 = Comment.objects.create(author=self.second_user, text="sembra buona, ma non mi fido")

        self.recipe.comments.add(self.comment1)


    def test_tag_serializer(self):
        serializer = TagSerializer(instance=self.tag1)
        self.assertEqual(serializer.data["name"], "Vegan")
        self.assertIn("id", serializer.data)

    def test_ingredient_serializer(self):
        serializer = IngredientSerializer(instance=self.ingredient1)
        self.assertEqual(serializer.data["name"], "Sugar")
        self.assertIn("id", serializer.data)

    def test_rating_serializer(self):
        # Testa il serializer
        serializer = RatingSerializer(instance=self.rating)

        # Verifica i valori
        self.assertEqual(serializer.data['rating'], 5)
        self.assertEqual(serializer.data['recipe']['title'], self.recipe.title)
        self.assertEqual(serializer.data['author']['username'], self.user.username)

    def test_rating_serializer_error(self):
        # test errato
        self.rating.rating = 0
        serializer = RatingSerializer(data=self.rating)
        self.assertFalse(serializer.is_valid(), serializer.errors)


    def test_recipe_ingredients_serializer(self):
        serializer = RecipeIngredientsSerializer(instance=self.recipe_ingredient1)
        data = serializer.data
        self.assertEqual(data["ingredient"]["name"], "Sugar")
        self.assertEqual(data["quantity"], "3.00")
        self.assertEqual(data["unit"], "A")

    def test_recipe_serializer_serialization(self):
        serializer = RecipeSerializer(instance=self.recipe)
        data = serializer.data
        print(data)
        self.assertEqual(data["ratings"], 2)
        self.assertEqual(data["title"], "Chocolate Cake")
        self.assertEqual(data["author"]['username'], str(self.user))
        self.assertEqual(len(data["ingredients"]), 2)
        self.assertEqual(data["ingredients"][0]["ingredient"]["name"], "Sugar")

    def test_recipe_serializer_deserialization(self):
        recipe_data = {
            "title": "New Recipe",
            "description": "A new delicious recipe",
            "preparation_time": 30,
            "difficulty": 2,
            "steps": "Step 1\nStep 2",
            "is_public": True,
            "tags": [{"name": "Vegetarian"}],
            "ingredients": [{"ingredient": {"name": "Butter"}, "quantity": "2.50", "unit": "g"}]
        }

        serializer = RecipeSerializer(data=recipe_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        recipe = serializer.save(author=self.user)

        self.assertEqual(recipe.title, "New Recipe")
        self.assertEqual(recipe.tags.count(), 1)
        self.assertEqual(recipe.ingredients.count(), 1)
        self.assertEqual(recipe.author, self.user)

    def __create_test_image__(self):
        img = Image.new("RGB", (100, 100), color="red")  # Creazione di un'immagine RGB 100x100
        img_io = BytesIO()
        img.save(img_io, format="JPEG")  # Salva l'immagine nel formato JPEG
        img_io.seek(0)  # Torna all'inizio del buffer
        return SimpleUploadedFile("test_image.jpg", img_io.read(), content_type="image/jpeg")

    def test_recipe_image_serializer(self):
        # Simula un file immagine
        uploaded_image = self.__create_test_image__()

        # Dati di input per il serializer
        image_data = {
            "image": uploaded_image,
            "description": "An image of the recipe",
            "recipe": self.recipe.id,
        }

        # Test della deserializzazione
        serializer = RecipeImageSerializer(data=image_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        recipe_image = serializer.save()

        # Verifica che i dati siano stati salvati correttamente
        self.assertEqual(recipe_image.description, "An image of the recipe")
        self.assertEqual(recipe_image.recipe, self.recipe)
        self.assertIn("test_image", recipe_image.image.name)

        # Test della serializzazione
        serialized_data = RecipeImageSerializer(recipe_image).data
        self.assertEqual(serialized_data["description"], "An image of the recipe")
        self.assertEqual(serialized_data["recipe"], self.recipe.id)
        self.assertTrue("test_image.jpg" in serialized_data["image"])

        media_root = settings.MEDIA_ROOT
        recipe_images_dir = os.path.join(media_root, "recipe_images")
        if os.path.exists(recipe_images_dir):
            for file_name in os.listdir(recipe_images_dir):
                if file_name.startswith("test_image"):
                    os.remove(os.path.join(recipe_images_dir, file_name))


    def test_added_image_to_recipe_serializer(self):
        recipe_data = {
            "title": "New Recipe",
            "description": "A new delicious recipe",
            "preparation_time": 30,
            "difficulty": 2,
            "steps": "Step 1\nStep 2",
            "is_public": True,
            "tags": [{"name": "Vegetarian"}],
            "ingredients": [{"ingredient": {"name": "Butter"}, "quantity": "2.50", "unit": "g"}]
        }
        # creo la ricetta
        serializer_recipe = RecipeSerializer(data=recipe_data)
        self.assertTrue(serializer_recipe.is_valid(), serializer_recipe.errors)
        serializer_recipe.save(author=self.user)


        # carico la foto
        uploaded_image = self.__create_test_image__()
        image_data = {
            "image": uploaded_image,
            "description": "An image of the recipe",
            "recipe": serializer_recipe.instance.id,
        }
        serializer = RecipeImageSerializer(data=image_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()

        # Recupera la ricetta aggiornata
        updated_recipe = Recipe.objects.get(id=serializer_recipe.instance.id)

        # Serializza nuovamente la ricetta
        serializer_recipe = RecipeSerializer(updated_recipe)

        # Stampa il contenuto del serializer
        print(serializer_recipe.data)

        found_image = RecipeImage.objects.filter(recipe=serializer_recipe.instance.id).first()
        if not found_image:
            print("image not found")


        self.assertEqual(serializer_recipe.data["images"][0]["description"], "An image of the recipe")

    def test_comment_serializer(self):
        # Creazione di un commento
        comment = Comment.objects.create(
            author=self.user,
            recipe=self.recipe,
            text="This is a test comment.",
        )

        # Test della serializzazione
        serialized_data = CommentSerializer(comment).data
        self.assertEqual(serialized_data["text"], "This is a test comment.")
        self.assertEqual(serialized_data["author"]["username"], self.user.username)
        self.assertEqual(serialized_data["recipe"]["title"], self.recipe.title)

        # Test della deserializzazione
        comment_data = {
            "text": "Another test comment.",
            # Il campo recipe è read-only, quindi non è richiesto qui
        }

        # Fornisci il contesto con l'utente autenticato
        serializer = CommentSerializer(data=comment_data, context={"request": {"user": self.user}})
        self.assertTrue(serializer.is_valid(), serializer.errors)
        created_comment = serializer.save(author=self.user, recipe=self.recipe)

        # Verifica che i dati siano stati salvati correttamente
        self.assertEqual(created_comment.text, "Another test comment.")
        self.assertEqual(created_comment.recipe, self.recipe)
        self.assertEqual(created_comment.author, self.user)