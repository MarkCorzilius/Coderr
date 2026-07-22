from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from orders_app.models import Order
from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token


class BaseOrderDeleteTestCase(APITestCase):

    def setUp(self):
        self.staff_user = User.objects.create_user(
            username="staff-customer",
            email="staffcustomer@test.com",
            password="test123",
            type="customer",
            is_staff=True,
            )

        self.normal_user = User.objects.create_user(
            username="normal-customer",
            email="normalcustomer@test.com",
            password="test123",
            type="customer",
            )
        
        self.offer = Offer.objects.create(
            creator=self.normal_user,
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
            offer_detail_id=self.offer.id
            )
        
        self.staff_token = Token.objects.create(user=self.staff_user)
        self.normal_token = Token.objects.create(user=self.normal_user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        self.url = reverse('order-detail', kwargs={'pk': self.order.id})
        self.response = self.client.delete(self.url)


class OrderDeleteSuccessTests(BaseOrderDeleteTestCase):

    def setUp(self):
        super().setUp()

    def test_delete_order_returns_204(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_deleted_order_disappeared(self):
        self.assertFalse(Order.objects.filter(id=self.order.id))


class OrderDeleteAuthenticationTests(BaseOrderDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()

    def test_unauthenticated_user_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderDeleteAuthorizationTests(BaseOrderDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        self.response = self.client.delete(self.url)

    def test_user_is_not_staff_gets_403(self):
        self.assertFalse(self.normal_user.is_staff)
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_persist(self):
        self.assertTrue(Order.objects.filter(id=self.order.id).exists())


class OrderDeleteNotFoundTests(BaseOrderDeleteTestCase):

    def setUp(self):
        super().setUp()
        url = reverse('order-detail', kwargs={'pk': 9999})
        self.response = self.client.delete(url)

    def test_delete_unreal_order_returns_404(self):
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

    
