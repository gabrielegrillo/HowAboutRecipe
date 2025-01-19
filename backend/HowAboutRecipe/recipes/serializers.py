from rest_framework import serializers
from recipes.models import Tag, Ingredient, Recipe, RecipeImage, RecipeIngredients, Comment, Rating
from users import serializers as user_serializers
from django.urls import reverse

# recipeimage e comment
# https://www.django-rest-framework.org/api-guide/relations/
# https://adityash97.medium.com/drf-serializers-serializer-saving-many-to-many-relationships-made-simple-22efdfe6da8a

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']


class RecipeIngredientsSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredients
        fields = ['ingredient', 'quantity', 'unit']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('Quantity must be greater than 0.')
        return value


    def validated_unit(self, value):
        if value is None or value == '':
            return value

        accepted_units = ['g', 'kg', 'ml', 'l', 'tbsp', 'tsp', 'cup']
        if value not in accepted_units:
            raise serializers.ValidationError(f"Unit {value} is not accepted.")
        return value


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
        fields = ['id', 'image', 'description']



class CommentSerializer(serializers.ModelSerializer):
    author = user_serializers.UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created_at']
        read_only_fields = ['author', 'id']


class RecipeSerializer(serializers.ModelSerializer):
    author = user_serializers.UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    ingredients = RecipeIngredientsSerializer(source='recipeingredients_set', many=True, read_only=True)
    images = RecipeImageSerializer(many=True, read_only=True)
    average_rating = serializers.ReadOnlyField()
    comments = CommentSerializer(many=True, read_only=True)
    ratings = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'id', 'author', 'title', 'description', 'preparation_time',
            'difficulty', 'steps', 'is_public', 'approved', 'created_at',
            'tags', 'ingredients', 'images', 'ratings', 'average_rating', 'comments'
        ]
        read_only_fields = ['author', 'average_rating', 'id', 'ratings', 'comments']

    def get_ratings(self, obj):
        return obj.ratings.count()

    def create(self, validated_data):
        tags_data = self.initial_data.get('tags', [])
        ingredients_data = self.initial_data.get('ingredients', [])

        recipe = Recipe.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            recipe.tags.add(tag)

        for ingredient_data in ingredients_data:
            ingredient, _ = Ingredient.objects.get_or_create(**ingredient_data['ingredient'])
            RecipeIngredients.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )

        return recipe

    def update(self, instance, validated_data):
        tags_data = self.initial_data.get('tags', [])
        ingredients_data = self.initial_data.get('ingredients', [])

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.preparation_time = validated_data.get('preparation_time', instance.preparation_time)
        instance.difficulty = validated_data.get('difficulty', instance.difficulty)
        instance.steps = validated_data.get('steps', instance.steps)
        instance.is_public = validated_data.get('is_public', instance.is_public)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            instance.tags.add(tag)

        RecipeIngredients.objects.filter(recipe=instance).delete()
        for ingredient_data in ingredients_data:
            ingredient, _ = Ingredient.objects.get_or_create(**ingredient_data['ingredient'])
            RecipeIngredients.objects.create(
                recipe=instance,
                ingredient=ingredient,
                quantity=ingredient_data['quantity'],
                unit=ingredient_data['unit']
            )

        return instance


class RatingSerializer(serializers.ModelSerializer):
    author = user_serializers.UserSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ['id', 'author', 'recipe', 'rating']
        read_only_fields = ['id', 'author']

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError('Rating must be between 0 and 5.')
        return value
