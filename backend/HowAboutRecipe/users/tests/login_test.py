from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model


class LoginTests(APITestCase):
    def setUp(self):
        self.registration_url = '/api/users/register/'
        self.login_url = '/api/users/login/'

        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'Mario',
            'last_name': 'Rossi',
        }
        self.client.post(self.registration_url, self.user_data, format='json')

    def test_user_login_success(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_invalid_credentials(self):
        login_data = {
            'username': 'wronguser',
            'password': 'testpassword123',
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['detail'], 'No active account found with the given credentials')