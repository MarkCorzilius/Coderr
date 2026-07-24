from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User


class RegisterTests(APITestCase):
    """Test suite for the registration endpoint."""

    def setUp(self):
        """Set up a test user, token and API client."""

        self.password = "@test123"
        self.user = User.objects.create_user(
            username="Mark",
            email="markcorzilius@gmail.com",
            password=self.password,
            type="customer",
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("register")

    def test_register_success(self):
        """Test that a valid payload creates a new user."""

        data = {
            "username": "Valeria",
            "email": "valeria@gmail.com",
            "password": self.password,
            "repeated_password": self.password,
            "type": "customer",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="valeria@gmail.com").exists())

    def test_register_password_mismatch(self):
        """Test that mismatched passwords return 400."""

        data = {
            "username": "Valeria",
            "email": "valeria@gmail.com",
            "password": self.password,
            "repeated_password": "wrongPassword123",
            "type": "customer",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email="valeria@gmail.com").exists())

    def test_register_duplicate_email(self):
        """Test that duplicate email returns 400."""

        data = {
            "username": "AnotherName",
            "email": self.user.email,
            "password": self.password,
            "repeated_password": self.password,
            "type": "customer",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email=data["email"]).count(), 1)

    def test_register_success(self):
        self.data = {
            'username': 'Valeria',
            'email': 'valeria@gmail.com',
            'password': self.password,
            'repeated_password': self.password,
            'type': 'customer'
        }       
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='valeria@gmail.com').exists())

    def test_register_password_mismatch(self):
        data = {
            'username': 'Valeria',
            'email': 'valeria@gmail.com',
            'password': self.password,
            'repeated_password': 'wrongPassword123',
            'type': 'customer'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email='valeria@gmail.com').exists())

    def test_register_duplicate_email(self):
        data = {
            'username': 'AnotherName',
            'email': self.user.email,
            'password': self.password,
            'repeated_password': self.password,
            'type': 'customer'
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email=data['email']).count(), 1)