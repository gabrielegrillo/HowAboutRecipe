from django.urls import path
from .views import (UserRegistrationView, UserActivationView, CustomTokenObtainPairView, UserDetail)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'), # register
    path('activate/<uid>/<token>/', UserActivationView.as_view(), name='activate'), # activate account from email verification
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),  # Login
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # Refresh token
    path("detail/", UserDetail.as_view(), name="user_detail"), # detail user
]