from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User


class ProfilesListTests(APITestCase):
    """Test suite for business and customer profile list endpoints."""

    def setUp(self):
        """Set up business and customer users with tokens."""

        self.url_customer = reverse("profiles-customer-list")
        self.url_business = reverse("profiles-business-list")
        self.business_user = User.objects.create_user(
            email="business@test.com", username="business",
            password="Password123!", type="business",
        )
        self.customer_user = User.objects.create_user(
            email="customer@test.com", username="customer",
            password="Password123!", type="customer",
        )
        self.business_token = Token.objects.create(user=self.business_user)
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()

    def test_business_profiles_list_success(self):
        """Test that business profile list returns only business profiles."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        response = self.client.get(self.url_business)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for profile in response.data:
            self.assertEqual(profile["type"], "business")
        self.assertGreater(len(response.data), 0)

    def test_unauth_business_access(self):
        """Test that unauthenticated request to business list returns 401."""

        response = self.client.get(self.url_business)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_list_success(self):
        """Test that customer profile list returns only customer profiles."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.customer_token.key)
        response = self.client.get(self.url_customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for profile in response.data:
            self.assertEqual(profile["type"], "customer")
        self.assertGreater(len(response.data), 0)

    def test_unauth_customer_access(self):
        """Test that unauthenticated request to customer list returns 401."""

        response = self.client.get(self.url_customer)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
