from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from recipes.models import Recipe, Tag, Ingredient, RecipeImage
from recipes.serializers import RecipeSerializer, RecipeImageSerializer, TagSerializer, IngredientSerializer
from recipes.permissions import IsAuthorOrReadOnly
from users.models import User


class RecipeDetailView(APIView):
    """
    View to show details of a given Recipe
    - view a recipe (GET) done
    - edit a recipe (PUT) done
    - delete a recipe (DELETE) done

    Requires authentication in order to
    """
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticatedOrReadOnly]
    def get(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(id=kwargs.get("pk")).first()
        if recipe and recipe.is_public:
            serializer = self.serializer_class(recipe, many=False)
            return Response(serializer.data)
        elif recipe and (not recipe.is_public or not recipe.approved) and (recipe.author != request.user or not request.user.is_superuser):
            return Response(status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(id=kwargs.get("pk")).first()
        if not recipe:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if recipe.author != request.user and not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(recipe, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        recipe = Recipe.objects.filter(id=kwargs.get("pk"))
        if not recipe:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif (recipe.author != request.user) and (not request.user.is_superuser):
            return Response(status=status.HTTP_403_FORBIDDEN)

        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





# class ImageView(APIView):
#     serializer_class = RecipeImageSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#
#     def get(self, request, *args, **kwargs):
#
#         img = Image.objects.filter(id=kwargs.get("id")).first()



class ImageDetailView(APIView):
    pass


class RecipesHomeView(ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny]
    queryset = Recipe.objects.filter(is_public=True)[:10]


class RecipesUserView(ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Recipe.objects.filter(author=user, is_public=True)

    def get(self, request, *args, **kwargs):
        recipes = self.get_queryset()
        return Response(self.serializer_class(recipes, many=True).data, status=status.HTTP_200_OK)


class RecipesTagView(APIView):
    serializer_class = RecipeSerializer
    permission_classes = [AllowAny,]

    def get(self, request, *args, **kwargs):
        tag_name = kwargs.get('name').capitalize()
        tag = Tag.objects.filter(name=tag_name).first()

        if not tag:
            return Response({"detail": "Tag not found."}, status=status.HTTP_404_NOT_FOUND)

        recipes = Recipe.objects.filter(tags=tag, is_public=True)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)