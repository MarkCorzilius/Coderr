from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class BaseCompletedOrderCountTestCase(APITestCase):
    """Shared test data for the completed-order-count endpoint tests."""

    def setUp(self):
        """Set up users, offer, three orders with mixed statuses, and tokens."""

        self.customer_user = User.objects.create_user(
            username="customer", email="customer@test.com", password="test123", type="customer"
        )
        self.business_user = User.objects.create_user(
            username="business", email="business@test.com", password="test123", type="business"
        )
        self.second_business_user = User.objects.create_user(
            username="second-business", email="secondbusiness@test.com",
            password="test123", type="business"
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
        base = dict(
            customer_user=self.customer_user, business_user=self.business_user,
            title=self.offer_details[0].title, revisions=self.offer_details[0].revisions,
            delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
            price=self.offer_details[0].price, features=self.offer_details[0].features,
            offer_type=self.offer_details[0].offer_type,
        )
        self.orders = [
            Order.objects.create(**base, status="in_progress"),
            Order.objects.create(**base, status="completed"),
            Order.objects.create(**base, status="cancelled"),
        ]
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.second_business_token = Token.objects.create(user=self.second_business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        self.url = reverse("completed-order-count", kwargs={"business_user_id": self.business_user.id})
        self.response = self.client.get(self.url)


class CompletedOrderCountSuccessTests(BaseCompletedOrderCountTestCase):
    """Test successful completed order count retrieval."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_order_count_returns_200(self):
        """Test that the endpoint returns 200 OK."""

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_order_count_is_correct(self):
        """Test that exactly one completed order is counted."""

        self.assertEqual(self.response.data["completed_order_count"], 1)

    def test_order_count_returns_expected_field(self):
        """Test that the response contains the completed_order_count field."""

        self.assertIn("completed_order_count", self.response.data.keys())

    def test_zero_orders_returns_0_count(self):
        """Test that a business user with no completed orders gets a count of zero."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.second_business_token.key)
        url = reverse("completed-order-count", kwargs={"business_user_id": self.second_business_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed_order_count"], 0)

    def test_counting_only_completed_orders(self):
        """Test that only completed orders contribute to the count."""

        self.assertEqual(self.response.data["completed_order_count"], 1)


class CompletedOrderCountAuthenticationTests(BaseCompletedOrderCountTestCase):
    """Test that unauthenticated users cannot access the completed order count."""

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

        self.second_business_user = User.objects.create_user(
            username="second-business",
            email="secondbusiness@test.com",
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

        self.orders = [
            Order.objects.create(
                customer_user=self.customer_user,
                business_user=self.business_user,
                title=self.offer_details[0].title,
                revisions=self.offer_details[0].revisions,
                delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
                price=self.offer_details[0].price,
                features=self.offer_details[0].features,
                offer_type=self.offer_details[0].offer_type,
                status="in_progress",
            ),
            Order.objects.create(
                customer_user=self.customer_user,
                business_user=self.business_user,
                title=self.offer_details[0].title,
                revisions=self.offer_details[0].revisions,
                delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
                price=self.offer_details[0].price,
                features=self.offer_details[0].features,
                offer_type=self.offer_details[0].offer_type,
                status="completed",
            ),
            Order.objects.create(
                customer_user=self.customer_user,
                business_user=self.business_user,
                title=self.offer_details[0].title,
                revisions=self.offer_details[0].revisions,
                delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
                price=self.offer_details[0].price,
                features=self.offer_details[0].features,
                offer_type=self.offer_details[0].offer_type,
                status="cancelled",
                ),
                ]
        
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.second_business_token = Token.objects.create(user=self.second_business_user
)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        self.url = reverse('completed-order-count', kwargs={'business_user_id': self.business_user.id})
        self.response = self.client.get(self.url)



class CompletedOrderCountSuccessTests(BaseCompletedOrderCountTestCase):

    def setUp(self):
        super().setUp()

    def test_order_count_returns_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_order_count_is_correct(self):
        self.assertEqual(self.response.data['completed_order_count'], 1)

    def test_order_count_returns_expected_field(self):
        self.assertIn('completed_order_count', self.response.data.keys())

    def test_zero_orders_returns_0_count(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.second_business_token.key)
        url = reverse('completed-order-count', kwargs={'business_user_id': self.second_business_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_order_count'], 0)

    def test_counting_only_in_progress_orders(self):
        self.assertEqual(self.response.data['completed_order_count'], 1)


class CompletedOrderCountAuthenticationTests(BaseCompletedOrderCountTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.get(self.url)

    def test_unauthenticated_user_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)