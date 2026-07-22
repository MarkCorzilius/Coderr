from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from orders_app.models import Order
from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token


class BaseOrderUpdateTestCase(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer",
            email="customer@test.com",
            password="test123",
            type="customer",
            )

        self.business_user = User.objects.create_user(
            username="business",
            email="business@test.com",
            password="test123",
            type="business",
            )

        self.foreign_business_user = User.objects.create_user(
            username="foreign_business_user",
            email="business@test.com",
            password="test123",
            type="business",
            )

        self.offer = Offer.objects.create(
            creator=self.business_user,
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
            offer_detail_id=self.offer_details[1].id
            )
        
        self.business_token = Token.objects.create(user=self.business_user)
        self.foreign_business_token = Token.objects.create(user=self.foreign_business_user)
        self.customer_token = Token.objects.create(user=self.customer_user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        self.payload = {
            "status": "completed"
        }
        self.url = reverse('order-detail', kwargs={'pk': self.order.id})
        self.response = self.client.patch(self.url, self.payload, format='json')



class OrderUpdateSuccessTests(BaseOrderUpdateTestCase):

    def setUp(self):
        super().setUp()

    def test_order_update_returns_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_order_updated_status_in_db(self):
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "completed")

    def test_updated_at_did_update(self):
        old_updated_at = self.order.updated_at
        self.order.refresh_from_db()
        self.assertGreater(self.order.updated_at, old_updated_at)


class OrderUpdateAuthenticationTests(BaseOrderUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()

    def test_unauthenticated_user_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OrderUpdateAuthorizationTests(BaseOrderUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        self.response = self.client.patch(self.url, self.payload, format='json')

    def test_customer_gets_403(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_business_user_not_owning_order_gets_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.foreign_business_token.key)
        response = self.client.patch(self.url, self.payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrderUpdateValidationTests(BaseOrderUpdateTestCase):

    def setUp(self):
        super().setUp()

    def test_wrong_status_value_returns_400(self):
        wrong_payload = {
            "status": "wrongStatus"
        }
        url = reverse('order-detail', kwargs={'pk': self.order.id})
        response = self.client.patch(url, wrong_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_disallowed_field_returns_400(self):
        payload = {
            "price": 9999
            }
        response = self.client.patch(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderUpdateNotFoundTests(BaseOrderUpdateTestCase):

    def setUp(self):
        super().setUp()
        url = reverse('order-detail', kwargs={'pk': 9999})
        self.response = self.client.patch(url, self.payload, format='json')

    def test_unreal_order_returns_404(self):
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

    