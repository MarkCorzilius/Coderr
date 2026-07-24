from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from reviews_app.models import Review


class BaseReviewCreateTestCase(APITestCase):
    """Shared test data for review creation endpoint tests."""

    def setUp(self):
        """Set up users, offer, order, tokens, and POST payload."""

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
        ]
        Order.objects.create(
            customer_user=self.customer_user, business_user=self.business_user,
            title=self.offer_details[0].title, revisions=self.offer_details[0].revisions,
            delivery_time_in_days=self.offer_details[0].delivery_time_in_days,
            price=self.offer_details[0].price, features=self.offer_details[0].features,
            offer_type=self.offer_details[0].offer_type,
        )
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.customer_token.key)
        self.url = reverse("review-list")
        self.expected_fields = {
            "id", "business_user", "reviewer", "rating", "description", "created_at", "updated_at"
        }
        self.payload = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!",
        }


class ReviewCreateSuccessTests(BaseReviewCreateTestCase):
    """Test successful review creation by a customer user."""

    def setUp(self):
        """Set up and fire POST request."""

        super().setUp()
        self.response = self.client.post(self.url, self.payload, format="json")

    def test_create_returns_201(self):
        """Test that creating a review returns 201 Created."""

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_create_contains_all_expected_fields(self):
        """Test that the response contains all required fields."""

        self.assertEqual(set(self.response.data.keys()), self.expected_fields)


class ReviewCreateAuthenticationTests(BaseReviewCreateTestCase):
    """Test that unauthenticated users cannot create reviews."""

    def setUp(self):
        """Set up with cleared credentials and fire POST request."""

        super().setUp()
        self.client.credentials()
        self.response = self.client.post(self.url, self.payload, format="json")

    def test_unauthenticated_post_returns_401(self):
        """Test that unauthenticated request returns 401."""

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewCreateAuthorizationTests(BaseReviewCreateTestCase):
    """Test that business users cannot create reviews."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_only_customer_can_let_review(self):
        """Test that a business user receives 403 Forbidden."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.business_token.key)
        response = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReviewCreateValidationTests(BaseReviewCreateTestCase):
    """Test validation errors on review creation."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_only_one_review_per_person(self):
        """Test that a second review for the same business returns 400."""

        response1 = self.client.post(self.url, self.payload, format="json")
        response2 = self.client.post(self.url, self.payload, format="json")
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            Review.objects.filter(
                reviewer=self.customer_user, business_user=self.business_user
            ).count(),
            1,
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
