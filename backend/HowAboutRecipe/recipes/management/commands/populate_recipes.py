from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from recipes.models import Recipe, Ingredient, Tag, Comment, Rating, RecipeIngredients
from users.models import User
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Seleziona utenti esistenti
        user1 = User.objects.filter(id=3).first()
        user2 = User.objects.filter(id=4).first()

        if not user1 or not user2:
            self.stdout.write("Errore: Non sono stati trovati utenti con ID 3 e 4.")
            return

        # Crea tag
        tags = [
            Tag.objects.get_or_create(name="Dessert")[0],
            Tag.objects.get_or_create(name="Breakfast")[0],
            Tag.objects.get_or_create(name="Healthy")[0],
            Tag.objects.get_or_create(name="Quick")[0],
            Tag.objects.get_or_create(name="Vegetarian")[0],
        ]

        # Crea ingredienti
        ingredient_names = [
            "Flour", "Sugar", "Milk", "Eggs", "Butter", "Salt",
            "Tomatoes", "Cheese", "Spinach", "Chicken", "Cocoa Powder",
            "Lasagna Sheets", "Coconut Milk", "Garlic", "Bread",
            "Parmesan Cheese", "Croutons", "Carrots", "Broccoli",
            "Bell Peppers", "Soy Sauce", "Bananas", "Honey", "Pancetta",
            "Quinoa", "Lemon", "Arborio Rice", "Mushrooms", "Onion", "Beef",
            "Potatoes", "Beef Broth",  # ingredienti già esistenti
            "Tofu", "Avocado", "Taco Shells", "Lettuce", "Salsa", "Sour Cream", "Salmon Fillets", "Olive Oil", "Tortilla"# nuovi ingredienti
        ]

        ingredients = {name: Ingredient.objects.get_or_create(name=name)[0] for name in ingredient_names}

        # Definisci le ricette
        recipes = [
            {
                "author": user1,
                "title": "Sweet Potato Fries",
                "description": "Crispy and healthy sweet potato fries, perfect as a snack or side dish.",
                "preparation_time": 30,
                "difficulty": 1,
                "steps": "1. Peel and cut the sweet potatoes into fries. 2. Toss with olive oil, salt, pepper, and garlic. 3. Bake in the oven at 200°C for 25-30 minutes.",
                "tags": ["Quick", "Healthy", "Vegetarian"],
                "ingredients": [
                    {"name": "Sweet Potatoes", "quantity": 2, "unit": "pieces"},
                    {"name": "Olive Oil", "quantity": 2, "unit": "tablespoons"},
                    {"name": "Salt", "quantity": 1, "unit": "teaspoon"},
                    {"name": "Pepper", "quantity": 1, "unit": "teaspoon"},
                    {"name": "Garlic", "quantity": 2, "unit": "cloves"},
                ],
            },
            {
                "author": user2,
                "title": "Chicken Caesar Wrap",
                "description": "A healthy and delicious wrap with chicken, Caesar dressing, and fresh lettuce.",
                "preparation_time": 20,
                "difficulty": 2,
                "steps": "1. Cook the chicken and slice it. 2. Spread Caesar dressing on a tortilla. 3. Add lettuce, croutons, parmesan cheese, and chicken. Wrap and serve.",
                "tags": ["Healthy", "Quick"],
                "ingredients": [
                    {"name": "Chicken", "quantity": 200, "unit": "grams"},
                    {"name": "Caesar Dressing", "quantity": 3, "unit": "tablespoons"},
                    {"name": "Lettuce", "quantity": 1, "unit": "head"},
                    {"name": "Croutons", "quantity": 50, "unit": "grams"},
                    {"name": "Parmesan Cheese", "quantity": 30, "unit": "grams"},
                    {"name": "Tortilla", "quantity": 2, "unit": "pieces"},
                ],
            }
        ]

        # Crea ricette
        for recipe_data in recipes:
            recipe = Recipe.objects.create(
                author=recipe_data["author"],
                title=recipe_data["title"],
                description=recipe_data["description"],
                preparation_time=recipe_data["preparation_time"],
                difficulty=recipe_data["difficulty"],
                steps=recipe_data["steps"],
                is_public=True,
                approved=True,
            )

            # Aggiungi tag
            for tag_name in recipe_data["tags"]:
                tag = Tag.objects.filter(name=tag_name).first()
                if tag:
                    recipe.tags.add(tag)

            # Aggiungi ingredienti
            for ingredient_data in recipe_data["ingredients"]:
                ingredient = ingredients.get(ingredient_data["name"])
                if ingredient:
                    RecipeIngredients.objects.create(
                        recipe=recipe,
                        ingredient=ingredient,
                        quantity=ingredient_data["quantity"],
                        unit=ingredient_data["unit"],
                    )



        self.stdout.write("Database popolato con successo!")