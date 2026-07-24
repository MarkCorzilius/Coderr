from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order


class BaseOrderDeleteTestCase(APITestCase):
    """Shared test data for order delete endpoint tests."""

    def setUp(self):
        """Set up staff, customer, business users, an order, and tokens."""

        self.staff_user = User.objects.create_user(
            username="staff-customer", email="staffcustomer@test.com",
            password="test123", type="customer", is_staff=True
        )
        self.customer_user = User.objects.create_user(
            username="customer", email="customer@test.com",
            password="test123", type="customer", is_staff=False
        )
        self.business_user = User.objects.create_user(
            username="business", email="business@test.com",
            password="test123", type="business", is_staff=False
        )
        self.offer = Offer.objects.create(
            user=self.customer_user, title="Professional Website Design",
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
        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title=self.offer_details[0].title,
            revisions=self.offer_details[0].revisions,
            delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
            price=self.offer_details[0].price,
            features=self.offer_details[0].features,
            offer_type=self.offer_details[0].offer_type,
        )
        self.staff_token = Token.objects.create(user=self.staff_user)
        self.business_token = Token.objects.create(user=self.customer_user)
        self.customer_token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.staff_token.key)
        self.url = reverse("order-detail", kwargs={"pk": self.order.id})


class OrderDeleteSuccessTests(BaseOrderDeleteTestCase):
    """Test successful order deletion by a staff user."""

    def setUp(self):
        """Set up and fire DELETE request."""

        super().setUp()
        self.response = self.client.delete(self.url)

    def test_delete_order_returns_204(self):
        """Test that delete returns 204 No Content."""

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleted_order_disappeared(self):
        """Test that the order no longer exists in the database."""

        self.assertFalse(Order.objects.filter(id=self.order.id))


class OrderDeleteAuthenticationTests(BaseOrderDeleteTestCase):
    """Test that unauthenticated users cannot delete orders."""

    def setUp(self):
        """Set up with cleared credentials and fire DELETE request."""

        super().setUp()
        self.client.credentials()
        self.response = self.client.delete(self.url)

    def test_unauthenticated_user_returns_401(self):
        """Test that unauthenticated request returns 401."""

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderDeleteAuthorizationTests(BaseOrderDeleteTestCase):
    """Test that non-staff users cannot delete orders."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_user_is_not_staff_gets_403(self):
        """Test that a non-staff user receives 403 Forbidden."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        response = self.client.delete(self.url)
        self.assertFalse(self.business_user.is_staff)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_persist(self):
        """Test that the order still exists after a failed delete."""

        self.assertTrue(Order.objects.filter(id=self.order.id).exists())


class OrderDeleteNotFoundTests(BaseOrderDeleteTestCase):
    """Test delete on a non-existent order."""

    def setUp(self):
        """Set up and fire DELETE for an unknown order ID."""

        super().setUp()
        url = reverse("order-detail", kwargs={"pk": 9999})
        self.response = self.client.delete(url)

    def test_delete_unreal_order_returns_404(self):
        """Test that deleting a non-existent order returns 404."""

        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

        self.customer_user = User.objects.create_user(
            username="customer",
            email="customer@test.com",
            password="test123",
            type="customer",
            is_staff=False
            )

        self.business_user = User.objects.create_user(
            username="business",
            email="business@test.com",
            password="test123",
            type="business",
            is_staff=False
            )
        
        
        self.offer = Offer.objects.create(
            user=self.customer_user,
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

        self.order = Order.objects.create(
            customer_user=self.customer_user,
            business_user=self.business_user,
            title=self.offer_details[0].title,
            revisions=self.offer_details[0].revisions,
            delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
            price=self.offer_details[0].price,
            features=self.offer_details[0].features,
            offer_type=self.offer_details[0].offer_type,
        )
        
        self.staff_token = Token.objects.create(user=self.staff_user)
        self.business_token = Token.objects.create(user=self.customer_user)
        self.customer_token = Token.objects.create(user=self.business_user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        self.url = reverse('order-detail', kwargs={'pk': self.order.id})


class OrderDeleteSuccessTests(BaseOrderDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.delete(self.url)

    def test_delete_order_returns_204(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleted_order_disappeared(self):
        self.assertFalse(Order.objects.filter(id=self.order.id))


class OrderDeleteAuthenticationTests(BaseOrderDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.delete(self.url)

    def test_unauthenticated_user_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderDeleteAuthorizationTests(BaseOrderDeleteTestCase):

    def setUp(self):
        super().setUp()

    def test_user_is_not_staff_gets_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.delete(self.url)
        self.assertFalse(self.business_user.is_staff)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_persist(self):
        self.assertTrue(Order.objects.filter(id=self.order.id).exists())


class OrderDeleteNotFoundTests(BaseOrderDeleteTestCase):

    def setUp(self):
        super().setUp()
        url = reverse('order-detail', kwargs={'pk': 9999})
        self.response = self.client.delete(url)

    def test_delete_unreal_order_returns_404(self):
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

    
