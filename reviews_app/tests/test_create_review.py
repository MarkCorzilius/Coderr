from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from orders_app.models import Order
from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token
from reviews_app.models import Review


class BaseReviewCreateTestCase(APITestCase):

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
        
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        self.url = reverse('review-list')

        self.expected_fields = {
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
            }

        self.payload = {
              "business_user": self.business_user.id,
              "rating": 4,
              "description": "Alles war toll!"
              }


class ReviewCreateSuccessTests(BaseReviewCreateTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_create_returns_201(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_create_contains_all_expected_fields(self):
        self.assertEqual(set(self.response.data.keys()), self.expected_fields)



class ReviewCreateAuthenticationTests(BaseReviewCreateTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_unauthenticated_post_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewCreateAuthorizationTests(BaseReviewCreateTestCase):

    def setUp(self):
        super().setUp()
        
    def test_only_customer_can_let_review(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.business_token.key)
        response = self.client.post(self.url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewCreateValidationTests(BaseReviewCreateTestCase):

    def setUp(self):
        super().setUp()

    def test_only_one_review_per_person(self):
        response1 = self.client.post(self.url, self.payload, format='json')
        response2 = self.client.post(self.url, self.payload, format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.filter(
            reviewer=self.customer_user,
            business_user=self.business_user
        ).count(), 1)
