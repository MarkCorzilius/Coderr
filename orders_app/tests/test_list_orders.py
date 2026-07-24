from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class BaseOrdersListTestCase(APITestCase):
    """Shared test data for order list endpoint tests."""

    def setUp(self):
        """Set up users, offer, one order, and fire GET request."""

        self.customer_user = User.objects.create_user(
            username="customer", email="customer@test.com", password="test123", type="customer"
        )
        self.business_user = User.objects.create_user(
            username="business", email="business@test.com", password="test123", type="business"
        )
        self.offer = Offer.objects.create(
            user=self.business_user, title="Professional Website Design",
            image=None, description="Modern web design packages."
        )
        self.offer_details = [
            OfferDetail.objects.create(
                offer=self.offer, title="Starter Package", revisions=2,
                delivery_time_in_days=5, price=300,
                features=["Landing Page Design", "Responsive Layout", "Basic UI Components"],
                offer_type="basic",
            ),
            OfferDetail.objects.create(
                offer=self.offer, title="Business Package", revisions=5,
                delivery_time_in_days=10, price=700,
                features=["Multi-page Website Design", "Responsive Layout", "Custom UI Components", "Design System"],
                offer_type="standard",
            ),
            OfferDetail.objects.create(
                offer=self.offer, title="Premium Package", revisions=10,
                delivery_time_in_days=15, price=1500,
                features=["Complete Website Design", "Advanced UI/UX Concept", "Custom Design System"],
                offer_type="premium",
            ),
        ]
        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title=self.offer_details[0].title,
            revisions=self.offer_details[0].revisions,
            delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
            price=self.offer_details[0].price,
            features=self.offer_details[0].features,
            offer_type=self.offer_details[0].offer_type,
        )
        self.token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("order-list")
        self.response = self.client.get(self.url)
        self.expected_fields = {
            "id", "customer_user", "business_user", "title", "revisions",
            "delivery_time_in_days", "price", "features", "offer_type",
            "status", "created_at", "updated_at",
        }


class OrderSuccessTests(BaseOrdersListTestCase):
    """Test successful order list retrieval."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_list_returns_200(self):
        """Test that listing orders returns 200 OK."""

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_list_is_not_empty(self):
        """Test that the response contains exactly one order."""

        self.assertEqual(len(self.response.data), 1)

    def test_list_contains_expected_fields(self):
        """Test that each order item has all expected fields."""

        self.assertEqual(set(self.response.data[0].keys()), self.expected_fields)


class OrdersListAuthenticationTests(BaseOrdersListTestCase):
    """Test that unauthenticated users cannot list orders."""

    def setUp(self):
        """Set up with cleared credentials and fire GET request."""

        super().setUp()
        self.client.credentials()
        self.response = self.client.get(self.url)

    def test_unauthenticated_user_returns_401(self):
        """Test that unauthenticated request returns 401."""

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.business_user = User.objects.create_user(
            username="business",
            email="business@test.com",
            password="test123",
            type="business",
            )

        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Professional Website Design",
            image=None,
            description="Modern web design packages for businesses that need a professional online presence.",
            )

        self.offer_details = [
            OfferDetail.objects.create(
                offer=self.offer,
                title="Starter Package",
                revisions=2,
                delivery_time_in_days=5,
                price=300,
                features=[
                    "Landing Page Design",
                    "Responsive Layout",
                    "Basic UI Components"
                    ],
                offer_type="basic",
                ),

            OfferDetail.objects.create(

                offer=self.offer,
                title="Business Package",
                revisions=5,
                delivery_time_in_days=10,
                price=700,
                features=[
                    "Multi-page Website Design",
                    "Responsive Layout",
                    "Custom UI Components",
                    "Design System"
                ],
                offer_type="standard",
                ),

            OfferDetail.objects.create(
                offer=self.offer,
                title="Premium Package",
                revisions=10,
                delivery_time_in_days=15,
                price=1500,
                features=[
                    "Complete Website Design",
                    "Advanced UI/UX Concept",
                    "Custom Design System",
                    "Prototype in Figma",
                    "Developer Handoff"
                ],
                offer_type="premium",
                ),
                ]

        Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title=self.offer_details[0].title,
            revisions=self.offer_details[0].revisions,
            delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
            price=self.offer_details[0].price,
            features=self.offer_details[0].features,
            offer_type=self.offer_details[0].offer_type,
        )
        
        self.token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('order-list')
        self.response = self.client.get(self.url)

        self.expected_fields = {
            "id",
            "customer_user",
            "business_user",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
            "status",
            "created_at",
            "updated_at",
            }


class OrderSuccessTests(BaseOrdersListTestCase):

    def setUp(self):
        super().setUp()

    def test_list_returns_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_list_is_not_empty(self):
        self.assertEqual(len(self.response.data), 1)

    def test_list_contains_expected_fields(self):
        self.assertEqual(set(self.response.data[0].keys()), self.expected_fields)

class OrdersListAuthenticationTests(BaseOrdersListTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.get(self.url)

    def test_unauthenticated_user_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)