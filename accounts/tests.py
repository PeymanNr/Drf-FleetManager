import unittest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
User = get_user_model()


class UserRegisterAPITest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('user-register')
        self.valid_payload = {
            'username': 'testuser232',
            'password': 'testpassword123P'
        }
        self.invalid_payload = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

    def test_user_registration_valid_data(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_invalid_data(self):
        response = self.client.post(self.register_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginAPITest(unittest.TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('user-login')
        self.valid_payload = {
            'username': 'testuser',
            'password': 'testpassword',
        }
        self.invalid_payload = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }

    def test_user_login_valid_data(self):
        response = self.client.post(self.login_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_data(self):
        response = self.client.post(self.login_url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
