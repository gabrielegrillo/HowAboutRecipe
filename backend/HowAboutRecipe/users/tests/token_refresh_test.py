from rest_framework.test import APITestCase
from rest_framework import status

class TokenRefreshTests(APITestCase):
    def setUp(self):
        self.registration_url = '/api/users/register/'  # Endpoint di registrazione
        self.refresh_url = '/api/users/token/refresh/'  # Endpoint di refresh del token

        # Crea un utente e ottieni i token
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.refresh_token = response.data['refresh_token']

    def test_refresh_token_success(self):
        response = self.client.post(self.refresh_url, {'refresh': self.refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_token_invalid(self):
        response = self.client.post(self.refresh_url, {'refresh': 'invalid_token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'Token is invalid or expired')