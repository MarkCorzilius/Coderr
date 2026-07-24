import copy

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail


class BaseOfferUpdateTestCase(APITestCase):
    """Shared test data for offer update endpoint tests."""

    def setUp(self):
        """Set up two business users, an offer with three details, and tokens."""

        self.user = User.objects.create_user(
            username="Tester", email="tester@gmail.com", password="test123", type="business"
        )
        self.user2 = User.objects.create_user(
            username="Tester2", email="tester2@gmail.com", password="test123", type="business"
        )
        self.offer = Offer.objects.create(
            user=self.user, title="Website Design", description="Professionelles Website-Design..."
        )
        OfferDetail.objects.create(
            offer=self.offer, title="Basic Design", revisions=2,
            delivery_time_in_days=5, price=100, features=["Logo Design"], offer_type="basic"
        )
        OfferDetail.objects.create(
            offer=self.offer, title="standard Design", revisions=2,
            delivery_time_in_days=5, price=100, features=["Logo Design"], offer_type="standard"
        )
        OfferDetail.objects.create(
            offer=self.offer, title="Premium Design", revisions=2,
            delivery_time_in_days=5, price=100, features=["Logo Design"], offer_type="premium"
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.token2 = Token.objects.create(user=self.user2)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.detail_url = reverse("offer-detail", kwargs={"pk": self.offer.id})
        self.payload = {
            "title": "Updated Grafikdesign-Paket",
            "description": "new description",
            "details": [
                {
                    "id": 1,
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": ["Logo Design", "Flyer"],
                    "offer_type": "basic",
                }
            ],
        }


class OfferUpdateSuccessTests(BaseOfferUpdateTestCase):
    """Test successful offer partial update by the owner."""

    def setUp(self):
        """Set up base test data."""

        super().setUp()

    def test_offer_update_returns_200(self):
        """Test that PATCH returns 200 and updates the offer."""

        response = self.client.patch(self.detail_url, self.payload)
        self.offer.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.offer.user, self.user)

    def test_only_updated_data_changed(self):
        """Test that only the patched fields are modified."""

        original_title = self.offer.title
        original_description = self.offer.description
        new_payload = copy.deepcopy(self.payload)
        new_payload.pop("title")
        self.client.patch(self.detail_url, new_payload)
        self.offer.refresh_from_db()
        offer = Offer.objects.first()
        self.assertEqual(offer.title, original_title)
        self.assertNotEqual(self.offer.description, original_description)


class OfferUpdateAuthorizationTests(BaseOfferUpdateTestCase):
    """Test that non-owner cannot update an offer."""

    def setUp(self):
        """Set up with second user credentials and fire PATCH request."""

        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        self.response = self.client.patch(self.detail_url, self.payload)

    def test_unauthorized_user_returns_403(self):
        """Test that a non-owner receives 403 Forbidden."""

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.offer.user, self.user2)


class OfferUpdateNotFoundTests(BaseOfferUpdateTestCase):
    """Test update on a non-existent offer."""

    def setUp(self):
        """Set up and fire PATCH for an unknown offer ID."""

        super().setUp()
        self.url = reverse("offer-detail", kwargs={"pk": 9999})
        self.response = self.client.patch(self.url, self.payload)

    def test_not_found_returns_404(self):
        """Test that patching a non-existent offer returns 404."""

        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)