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
                business_user=self.business_user,
                reviewer=self.customer_user,
                rating=3,
                description="Good overall, but could be improved."
            ),
            Review.objects.create(
                business_user=self.business_user,
                reviewer=self.customer_user,
                rating=4,
                description="Everything was great!"
            ),
            ]
        
        self.token = Token.objects.create(user=self.customer_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
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


class ReviewListSuccessTests(BaseReviewListTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_list_returns_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_list_is_filled(self):
        self.assertEqual(len(self.response.data), 3)

    def test_list_contains_all_expected_fields(self):
        self.assertEqual(set(self.response.data[0].keys()), self.expected_fields)



class ReviewListAuthenticationTests(BaseReviewListTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.get(self.url)

    def test_list_returns_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewListFilterTests(BaseReviewListTestCase):

    def setUp(self):
        super().setUp()
        

    def test_filter_by_business_user_id(self):
        response = self.client.get(
            self.url,
            {"business_user_id": self.business_user.id}
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        for review in response.data:
            self.assertEqual(review['business_user'], self.business_user.id)
        

    def test_filter_by_reviewer_id(self):
        response = self.client.get(
            self.url,
            {"reviewer_id": self.customer_user.id}
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        for review in response.data:
            self.assertEqual(review['reviewer'], self.customer_user.id)

    def test_filter_by_business_user_id_returns_empty_list(self):
        response = self.client.get(
            self.url,
            {"business_user_id": self.second_business_user.id}
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)



class ReviewListOrderingTests(BaseReviewListTestCase):

    def setUp(self):
        super().setUp()


    def test_ordering_by_updated_at_ascending(self):
        response = self.client.get(self.url, {"ordering": "updated_at"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = [review['id'] for review in response.data]
        self.assertEqual(ids, [
            self.reviews[0].id,
            self.reviews[1].id,
            self.reviews[2].id,
        ])

    def test_ordering_by_updated_at_descending(self):
        response = self.client.get(self.url, {"ordering": "-updated_at"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = [review['id'] for review in response.data]
        self.assertEqual(ids, [
            self.reviews[2].id,
            self.reviews[1].id,
            self.reviews[0].id,
            ])

    def test_ordering_by_rating_ascending(self):
        response = self.client.get(self.url, {"ordering": "rating"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ratings = [review['rating'] for review in response.data]
        self.assertEqual(ratings, [3, 4, 5])

    def test_ordering_by_rating_descending(self):
        response = self.client.get(self.url, {"ordering": "-rating"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ratings = [review['rating'] for review in response.data]
        self.assertEqual(ratings, [5, 4, 3])
