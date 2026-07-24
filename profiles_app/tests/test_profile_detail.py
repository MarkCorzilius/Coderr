from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User


class ProfileDetailTests(APITestCase):
    """Test suite for profile retrieve and update endpoint."""

    def setUp(self):
        """Set up a user, profile, token and API client."""

        self.password = "@test123"
        self.user = User.objects.create_user(
            username="Mark", email="markcorzilius@gmail.com",
            password=self.password, type="customer",
        )
        self.profile = self.user.profile
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("profile", kwargs={"user_id": self.profile.id})

    def test_get_profile_success(self):
        """Test that authenticated user can retrieve their profile."""

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"], self.user.id)

    def test_unauth_profile_access(self):
        """Test that unauthenticated request returns 401."""

        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_not_found(self):
        """Test that non-existent profile returns 404."""

        url = reverse("profile", kwargs={"user_id": 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_user_update_success(self):
        """Test that owner can update their profile via PATCH."""

        data = {"first_name": "Marki"}
        response = self.client.patch(self.url, data, format="json")
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.first_name, "Marki")


    def test_get_profile_success(self):
        response = self.client.get(self.url)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user.id)


    def test_unauth_profile_access(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_profile_not_found(self):
        url = reverse('profile', kwargs={'user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_logged_in_user_update_success(self):
        new_first_name = 'Marki'
        data = {
            'first_name': new_first_name,
        }
        response = self.client.patch(self.url, data, format='json')
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.first_name, new_first_name)


    def test_update_foreign_profile_error(self):
        self.client.credentials()
        new_first_name = 'Marki'
        data = {
            'first_name': new_first_name,
        }
        response = self.client.patch(self.url, data, format='json')
        self.profile.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_required_fields(self):
        data = {
            'username': '',
        }
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)