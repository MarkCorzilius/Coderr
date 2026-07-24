from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from orders_app.models import Order
from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token
from reviews_app.models import Review


class BaseReviewListTestCase(APITestCase):

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

        self.third_business_user = User.objects.create_user(
            username="third-business",
            email="thirdbusiness@test.com",
            password="test123",
            type="business",
            )
        self.foreign_business_user = User.objects.create_user(
            username="foreign-business",
            email="foreignbusiness@test.com",
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

        self.reviews = [
            Review.objects.create(
                business_user=self.business_user,
                reviewer=self.customer_user,
                rating=5,
                description="Excellent service!"
            ),
            Review.objects.create(
                business_user=self.second_business_user,
                reviewer=self.customer_user,
                rating=3,
                description="Good overall, but could be improved."
            ),
            Review.objects.create(
                business_user=self.third_business_user,
                reviewer=self.customer_user,
                rating=4,
                description="Everything was great!"
            ),
            ]
        
        self.token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('base-info')


class BaseInfoTests(BaseReviewListTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_returns_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_returns_correct_counts(self):
        data = self.response.data

        self.assertEqual(data["review_count"], 3)
        self.assertEqual(data["average_rating"], 4.0)
        self.assertEqual(data["business_profile_count"], 4)
        self.assertEqual(data["offer_count"], 1)


class EmptyBaseInfoTests(APITestCase):

    def setUp(self):
        self.url = reverse('base-info')

    def test_empty_db_returns_zeros(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["review_count"], 0)
        self.assertEqual(response.data["average_rating"], 0)
        self.assertEqual(response.data["business_profile_count"], 0)
        self.assertEqual(response.data["offer_count"], 0)

