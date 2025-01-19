from uuid import uuid4
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError

from users.models import User


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

class Recipe(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    preparation_time = models.PositiveSmallIntegerField()
    difficulty = models.PositiveSmallIntegerField()
    steps = models.TextField()

    is_public = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(Tag)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredients')

    comments = models.ManyToManyField(Comment)

    @property
    def average_rating(self):
        if self.ratings.exists():
            return sum(r.rating for r in self.ratings.all()) / len(self.ratings.all())
        return 0

    def __str__(self):
        return f"{self.title}"


class Rating(models.Model):
    id = models.IntegerField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')

    class Meta:
        constraints = [
            # one author can make one rating to a recipe
            models.UniqueConstraint(fields=['author', 'recipe'], name='unique_rating_per_recipe'),
        ]

    def __str__(self):
        return f"{self.author} rated {self.rating} on {self.recipe}"

class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.DecimalField(decimal_places=2, max_digits=10)
    unit = models.CharField(max_length=50, null=True, blank=True)


class RecipeImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    image = models.ImageField(upload_to="recipe_images/")
    description = models.CharField(max_length=255, blank=True, null=True)
    recipe = models.ForeignKey(Recipe, related_name='images', on_delete=models.CASCADE)