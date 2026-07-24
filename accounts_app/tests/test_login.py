from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User


class LoginTests(APITestCase):
    """Test suite for the login endpoint."""

    def setUp(self):
        """Set up a test user and API client."""

        self.username = "Mark"
        self.password = "test123"
        self.user = User.objects.create_user(
            username=self.username,
            email="markcorzilius@gmail.com",
            password=self.password,
            type="customer",
        )
        self.client = APIClient()
        self.url = reverse("login")

    def test_login_success(self):
        """Test successful login returns 200 with a token."""

        data = {"username": self.username, "password": self.password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertTrue(len(response.data["token"]) > 0)

    def test_login_wrong_password(self):
        """Test that wrong password returns 400."""

        data = {"username": self.username, "password": "wrongpassword"}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)

    def test_login_wrong_username(self):
        """Test that wrong username returns 400."""

        data = {"username": "WrongUsername", "password": self.password}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("token", response.data)