from django.urls import include, path
from . import views

urlpatterns = [
    # /recipes/...
    path('home/', views.RecipesHomeView.as_view(), name='home'),
    path('<str:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    path("user/<str:username>/", views.RecipesUserView.as_view(), name='recipes_user'),
    path("tag/<str:name>/", views.RecipesTagView.as_view(), name='recipes_tag'),

    # path('image/<int:pk>/', views.ImageDetailView.as_view(), name='image_detail'),
    # path('', views.Recipes.as_view(), name='recipes'),
    # path('<id>/ratings/' RecipeRating.as_view(), name='ratings' ),
]