from django.test import override_settings
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class UserRegistrationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')  # Nome della route per la registrazione
        self.activate_url_name = 'activate'  # Nome della route per l'attivazione

    def test_user_registration_and_email_sent(self):
        """
        Test that a user is registered and an activation email is sent.
        """
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post(self.register_url, data, format='json')

        # Controlla che l'utente sia stato creato
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.get(username='testuser')
        self.assertFalse(user.is_active)  # L'utente deve essere inattivo

        # Controlla che l'email sia stata inviata
        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Activate your account', mail.outbox[0].subject)

        # Controlla che l'email contenga il link di attivazione
        self.assertIn('/activate/', mail.outbox[0].body)

    def test_user_activation(self):
        """
        Test that a user can activate their account using the activation link.
        """
        # Crea un utente inattivo
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123',
            is_active=False
        )

        # Genera il token di attivazione e il link
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        activation_url = reverse(self.activate_url_name, kwargs={'uid': uid, 'token': token})

        response = self.client.get(activation_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_invalid_activation_link(self):
        """
        Test that an invalid activation link returns an error.
        """
        # Crea un utente inattivo
        user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123',
            is_active=False
        )

        # Usa un token errato
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        invalid_token = 'invalid-token'
        activation_url = reverse(self.activate_url_name, kwargs={'uid': uid, 'token': invalid_token})

        # Effettua una richiesta GET con il token non valido
        response = self.client.get(activation_url)

        # Controlla che l'utente non sia stato attivato
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user.refresh_from_db()
        self.assertFalse(user.is_active)
