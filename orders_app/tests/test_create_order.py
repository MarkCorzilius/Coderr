from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class BaseOrderCreateTestCase(APITestCase):
    """Shared test data for order creation endpoint tests."""

    def setUp(self):
        """Set up users, offer, details, tokens, and fire POST request."""

        self.customer_user = User.objects.create_user(
            username="customer", email="customer@test.com", password="test123", type="customer"
        )
        self.business_user = User.objects.create_user(
            username="business", email="business@test.com", password="test123", type="business"
        )
        self.offer = Offer.objects.create(
            user=self.business_user,
            title="Professional Website Design",
            image=None,
            description="Modern web design packages.",
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
        self.client = APIClient()
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.customer_token.key)
        self.url = reverse("order-list")
        self.payload = {"offer_detail_id": self.offer_details[0].id}
        self.response = self.client.post(self.url, self.payload, format="json")
        self.expected_fields = {
            "id", "customer_user", "business_user", "title", "revisions",
            "delivery_time_in_days", "price", "features", "offer_type",
            "status", "created_at", "updated_at",
        }


class OrderCreateSuccessTests(BaseOrderCreateTestCase):
    """Test successful order creation by a customer user."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_creating_order_returns_201(self):
        """Test that creating an order returns 201 Created."""

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_order_created_in_db(self):
        """Test that the order is persisted in the database."""

        self.assertEqual(Order.objects.count(), 1)

    def test_order_has_expected_fields(self):
        """Test that the response contains all required fields."""

        self.assertEqual(set(self.response.data.keys()), self.expected_fields)


class OrderCreateAuthenticationTests(BaseOrderCreateTestCase):
    """Test that unauthenticated users cannot create orders."""

    def setUp(self):
        """Set up with cleared credentials and fire POST request."""

        super().setUp()
        self.client.credentials()
        self.response = self.client.post(self.url, self.payload, format="json")

    def test_unauthenticated_user_returns_401(self):
        """Test that unauthenticated request returns 401."""

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderCreateAuthorizationTests(BaseOrderCreateTestCase):
    """Test that business users cannot create orders."""

    def setUp(self):
        """Set up with business token and fire POST request."""

        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        self.response = self.client.post(self.url, self.payload, format="json")

    def test_if_not_a_customer_returns_403(self):
        """Test that business user receives 403 Forbidden."""

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)


class OrderCreateValidationTests(BaseOrderCreateTestCase):
    """Test validation errors on order creation."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_order_with_no_offer_id_returns_400(self):
        """Test that omitting offer_detail_id returns 400."""

        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_detail_not_found(self):
        """Test that an unknown offer detail id returns 400."""

        response = self.client.post(self.url, {"offer_detail_id": 9999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderCreateSuccessTests(BaseOrderCreateTestCase):

    def setUp(self):
        super().setUp()

    def test_creating_order_returns_201(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_order_created_in_db(self):
        self.assertEqual(Order.objects.count(), 1)

    def test_order_has_expected_fields(self):
        self.assertEqual(set(self.response.data.keys()), self.expected_fields)


class OrderCreateAuthenticationTests(BaseOrderCreateTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_unauthenticated_user_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderCreateAuthorizationTests(BaseOrderCreateTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_if_not_a_customer_returns_403(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
        


class OrderCreateValidationTests(BaseOrderCreateTestCase):

    def setUp(self):
        super().setUp()

    def test_order_with_no_offer_id_returns_400(self):
        empty_payload = {}
        response = self.client.post(self.url, empty_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_offer_detail_not_found(self):
        payload = {
            "offer_detail_id": 9999,
            }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)