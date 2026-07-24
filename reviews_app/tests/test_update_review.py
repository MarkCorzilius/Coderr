from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from orders_app.models import Order
from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token
from reviews_app.models import Review


class BaseReviewUpdateTestCase(APITestCase):

    def setUp(self):
        self.customer_user = User.objects.create_user(
            username="customer",
            email="customer@test.com",
            password="test123",
            type="customer",
            )

        self.second_customer_user = User.objects.create_user(
            username="second-customer",
            email="secondcustomer@test.com",
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

        self.review = Review.objects.create(
            business_user=self.business_user,
            reviewer=self.customer_user,
            rating=5,
            description="Excellent service!"
            )
        
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.second_customer_token = Token.objects.create(user=self.second_customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.customer_token.key)
        self.url = reverse('review-detail', kwargs={'pk': self.review.id})

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
            "business_user": 1,
            "rating": 2,
            }


class ReviewUpdateSuccessTests(BaseReviewUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.patch(self.url, self.payload, format='json')

    def test_patch_returns_200(self):
        self.review.refresh_from_db()
        self.assertEqual(self.review.rating, 2)
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_database_updated(self):
        original_rating = self.review.rating
        original_description = self.review.description
        self.review.refresh_from_db()
        self.assertEqual(self.response.data['rating'], original_rating)
        self.assertEqual(self.response.data['description'], original_description)

    def test_patch_returns_expected_fields(self):
        self.assertEqual(set(self.response.data.keys()), self.expected_fields)

    def test_updated_at_works(self):
        original_update_at = self.review.updated_at
        self.review.refresh_from_db()
        self.assertEqual(self.response.data['updated_at'], original_update_at)


class ReviewUpdateAuthenticationTests(BaseReviewUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.patch(self.url, self.payload, format='json')

    def test_unauthenticated_patch_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewUpdateAuthorizationTests(BaseReviewUpdateTestCase):

    def setUp(self):
        super().setUp()

    def test_foreign_user_gets_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.second_customer_token.key)
        response = self.client.patch(self.url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        

class ReviewUpdateValidationTests(BaseReviewUpdateTestCase):

    def setUp(self):
        super().setUp()

    def test_update_wrong_payload_returns_400(self):
        payload = {
            "issues": "Noch besser als erwartet!"
            }
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        response = self.client.patch(url, payload, format='json')    

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 

    def test_update_business_user_returns_400(self):
        payload = {
            "business_user": 1
            }
        url = reverse('review-detail', kwargs={'pk': self.review.id})
        response = self.client.patch(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ReviewUpdateNotFoundTests(BaseReviewUpdateTestCase):

    def setUp(self):
        super().setUp()

    def test_review_not_found_returns_404(self):
        url = reverse('review-detail', kwargs={'pk': 9999})
        response = self.client.patch(url, self.payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)