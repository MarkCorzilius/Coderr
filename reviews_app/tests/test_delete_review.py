from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from orders_app.models import Order
from reviews_app.models import Review


class BaseReviewDeleteTestCase(APITestCase):
    """Shared test data for review delete endpoint tests."""

    def setUp(self):
        """Set up users, offer, order, a review, tokens, and authenticated client."""

        self.customer_user = User.objects.create_user(
            username="customer", email="customer@test.com", password="test123", type="customer"
        )
        self.second_customer_user = User.objects.create_user(
            username="second-customer", email="secondcustomer@test.com",
            password="test123", type="customer"
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
        self.review = Review.objects.create(
            business_user=self.business_user, reviewer=self.customer_user,
            rating=5, description="Excellent service!"
        )
        self.customer_token = Token.objects.create(user=self.customer_user)
        self.second_customer_token = Token.objects.create(user=self.second_customer_user)
        self.business_token = Token.objects.create(user=self.business_user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.customer_token.key)
        self.url = reverse("review-detail", kwargs={"pk": self.review.id})


class ReviewDeleteSuccessTests(BaseReviewDeleteTestCase):
    """Test successful review deletion by the reviewer."""

    def setUp(self):
        """Set up and fire DELETE request."""

        super().setUp()
        self.response = self.client.delete(self.url)

    def test_delete_returns_204(self):
        """Test that delete returns 204 No Content with no body."""

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(self.response.data)

    def test_deleted_review_no_longer_exists(self):
        """Test that the review is removed from the database."""

        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())


class ReviewDeleteAuthenticationTests(BaseReviewDeleteTestCase):
    """Test that unauthenticated users cannot delete reviews."""

    def setUp(self):
        """Set up with cleared credentials and fire DELETE request."""

        super().setUp()
        self.client.credentials()
        self.response = self.client.delete(self.url)

    def test_unauthenticated_delete_returns_401(self):
        """Test that unauthenticated request returns 401."""

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewDeleteAuthorizationTests(BaseReviewDeleteTestCase):
    """Test that only the review creator can delete a review."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_foreign_user_gets_403(self):
        """Test that a different user receives 403 Forbidden."""

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.second_customer_token.key)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Review.objects.filter(pk=self.review.pk).exists())


class ReviewDeleteNotFoundTests(BaseReviewDeleteTestCase):
    """Test delete on a non-existent review."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_review_not_found_returns_404(self):
        """Test that deleting a non-existent review returns 404."""

        url = reverse("review-detail", kwargs={"pk": 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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

class ReviewDeleteSuccessTests(BaseReviewDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.delete(self.url)

    def test_delete_returns_204(self):
        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(self.response.data)

    def test_deleted_review_no_longer_exists(self):
        self.assertFalse(
            Review.objects.filter(pk=self.review.pk).exists()
        )


class ReviewDeleteAuthenticationTests(BaseReviewDeleteTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.delete(self.url)

    def test_unauthenticated_delete_returns_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewDeleteAuthorizationTests(BaseReviewDeleteTestCase):

    def setUp(self):
        super().setUp()

    def test_foreign_user_gets_403(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.second_customer_token.key)
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(
            Review.objects.filter(pk=self.review.pk).exists()
            )
        

class ReviewDeleteNotFoundTests(BaseReviewDeleteTestCase):

    def setUp(self):
        super().setUp()

    def test_review_not_found_returns_404(self):
        url = reverse('review-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)