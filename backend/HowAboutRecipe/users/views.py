from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from jwt.utils import force_bytes
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from users import serializers
from users.models import User
from users.serializers import CustomTokenObtainPairSerializer


# Create your views here.

class UserRegistrationView(APIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(str(user.pk)))
            current_site = request.get_host()
            link = f"http://{current_site}/api/users/activate/{uid}/{token}/"

            subject = f'HowAboutRecipes: Hey {user.first_name}! Activate your account'
            # TODO: sostituire con HTML
            message = f'Hi {user.first_name},\n\nPlease click the link below to confirm your email and activate your account:\n\n{link}\n\nThank you!'
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email]
            )

            return Response({
                'message': 'User registered successfully! Please check your email to activate your account.',
                'user': {
                    'username': user.username,
                    'email': user.email
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        uid = kwargs.get('uid')
        token = kwargs.get('token')

        if not uid or not token:
            return Response({'error': 'Missing uid or token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid uid or user does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account successfully activated! You can now log in.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid or expired'}, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request, *args, **kwargs):
        user = request.user
        response = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        return Response(response, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer