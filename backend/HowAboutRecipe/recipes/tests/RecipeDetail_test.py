from rest_framework.test import APITestCase
from rest_framework import status
from recipes.models import Recipe, RecipeIngredients, Tag, Ingredient, Rating
from users.models import User

class RecipeDetailViewTestCase(APITestCase):
    def setUp(self):
        # Crea due utenti
        self.author = User.objects.create_user(username="author", password="password123")
        self.other_user = User.objects.create_user(username="other_user", password="password456")

        # Crea una ricetta pubblica e una privata
        self.tag1 = Tag.objects.create(name="Vegan")
        self.tag2 = Tag.objects.create(name="Gluten-Free")
        self.ingredient1 = Ingredient.objects.create(name="Sugar")
        self.ingredient2 = Ingredient.objects.create(name="Flour")

        self.public_recipe = Recipe.objects.create(
            title="Public Recipe",
            description="A simple public recipe",
            preparation_time=30,
            difficulty=2,
            steps="Step 1\nStep 2",
            author=self.author,
            is_public=True,
        )

        self.private_recipe = Recipe.objects.create(
            title="Private Recipe",
            description="A private recipe",
            preparation_time=45,
            difficulty=3,
            steps="Step 1\nStep 2\nStep 3",
            author=self.author,
            is_public=False,
        )

        self.public_recipe.tags.add(self.tag1);
        self.recipe_ingredient1 = RecipeIngredients.objects.create(
            recipe=self.public_recipe, ingredient=self.ingredient1, quantity=3, unit="A"
        )
        self.recipe_ingredient2 = RecipeIngredients.objects.create(
            recipe=self.public_recipe, ingredient=self.ingredient2, quantity=1, unit="m"
        )

        self.rating = Rating.objects.create(author=self.author, recipe=self.public_recipe, rating=5)

        # URL per accedere ai dettagli delle ricette
        self.public_recipe_url = f"/api/recipes/{self.public_recipe.id}/"
        self.private_recipe_url = f"/api/recipes/{self.private_recipe.id}/"

    def test_retrieve_public_recipe_as_unauthenticated_user(self):
        # Nessuna autenticazione, accede a una ricetta pubblica
        response = self.client.get(self.public_recipe_url)

        # Verifica che la risposta sia 200 OK e contenga i dati corretti
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.public_recipe.title)

    def test_retrieve_private_recipe_as_unauthenticated_user(self):
        # Nessuna autenticazione, accede a una ricetta privata
        response = self.client.get(self.private_recipe_url)

        # Verifica che la risposta sia 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_recipe_as_authenticated_user(self):
        # Autenticazione come un utente
        self.client.force_authenticate(user=self.author)
        response = self.client.get(self.public_recipe_url)

        # Verifica che la risposta sia 200 OK e contenga i dati corretti
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.public_recipe.title)

    def test_update_recipe_as_author(self):
        # Autenticazione come autore della ricetta
        self.client.force_authenticate(user=self.author)
        new_data = {"title": "Updated Recipe Title"}
        response = self.client.patch(self.public_recipe_url, new_data)

        # Verifica che la risposta sia 200 OK e che il titolo sia aggiornato
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.public_recipe.refresh_from_db()
        self.assertEqual(self.public_recipe.title, "Updated Recipe Title")

    def test_update_recipe_as_non_author(self):
        # Autenticazione come un altro utente
        self.client.force_authenticate(user=self.other_user)
        new_data = {"title": "Another Update"}
        response = self.client.patch(self.public_recipe_url, new_data)

        # Verifica che la risposta sia 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_recipe_as_author(self):
        # Autenticazione come autore della ricetta
        self.client.force_authenticate(user=self.author)
        response = self.client.delete(self.public_recipe_url)

        # Verifica che la risposta sia 204 No Content e che la ricetta sia eliminata
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Recipe.objects.filter(id=self.public_recipe.id).exists())

    def test_delete_recipe_as_non_author(self):
        # Autenticazione come un altro utente
        self.client.force_authenticate(user=self.other_user)
        response = self.client.delete(self.public_recipe_url)

        # Verifica che la risposta sia 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
