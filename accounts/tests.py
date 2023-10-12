import unittest
from django.test import Client
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class TokenMiddlewareTestCase(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user-register')
        self.login_url = reverse('user-login')
        self.user_data = {
            'username': 'testuser11',
            'password': 'testpassword11'
        }
        # self.user = User.objects.create_user(**self.user_data)
        # self.refresh_token = RefreshToken.for_user(self.user)

    def test_access_allowed_with_valid_token(self):
        response = self.client.post(self.register_url, data=self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        access_token = response.data.get('access')

        response = self.client.get(self.register_url, HTTP_AUTHORIZATION=f'Bearer {access_token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    # def test_access_denied_with_invalid_token(self):
    #     response = self.client.get(self.register_url, HTTP_AUTHORIZATION='Bearer INVALID_TOKEN')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    # def test_access_denied_without_token(self):
    #     response = self.client.get(self.register_url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
