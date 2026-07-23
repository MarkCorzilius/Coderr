from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from orders_app.models import Order
from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token


class BaseOrdersCountTestCase(APITestCase):

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

        self.second_business_user = User.objects.create_user(
            username="second-business",
            email="secondbusiness@test.com",
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
            offer_detail_id=self.offer_details[0].id,
            status='in_progres',
            )

        self.order2 = Order.objects.create(
            offer_detail_id=self.offer_details[0].id,
            status='completed',
            )

        self.order3 = Order.objects.create(
            offer_detail_id=self.offer_details[0].id,
            status='completed',
            )
        
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.second_business_token = Token.objects.create(user=self.second_business_user
)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        self.url = reverse('order-count', kwargs={'business_user_id': self.business_user.id})
        self.response = self.client.get(self.url)



class OrdersCountSuccessTests(BaseOrdersCountTestCase):

    def setUp(self):
        super().setUp()

    def test_order_count_returns_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_order_count_is_correct(self):
        self.assertEqual(self.response.data['order_count'], 1)

    def test_order_count_returns_expected_field(self):
        self.assertIn('order_count', self.response.data.keys())

    def test_zero_orders_returns_0_count(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.second_business_token.key)
        url = reverse('order-count', kwargs={'business_user_id': self.second_business_user.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 0)

    def test_counting_only_in_progress_orders(self):
        self.assertEqual(self.response.data['order_count'], 1)


class OrdersCountAuthenticationTests(BaseOrdersCountTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()

    def test_unauthenticated_user_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


#class OrdersCountAuthorizationTests(BaseOrdersCountTestCase):
#
#    def setUp(self):
#        super().setUp()
#        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.second_business_token.key)
#        self.response = self.client.get(self.url)
#
#    def test_not_owner_gets_403(self):
#        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)    
    

class OrdersCountNotFoundTests(BaseOrdersCountTestCase):

    def setUp(self):
        super().setUp()

    def test_business_user_not_found(self):
        url = reverse('order-count', kwargs={'business_user_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
