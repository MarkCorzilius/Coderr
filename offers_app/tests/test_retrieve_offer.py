from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail


class BaseOfferRetrieveTestCase(APITestCase):
    """Shared test data for offer retrieve endpoint tests."""

    def setUp(self):
        """Set up a user, offer with one detail, and authenticated client."""

        self.user = User.objects.create_user(
            username="Tester", email="tester@gmail.com", password="test123", type="customer"
        )
        self.offer = Offer.objects.create(
            user=self.user, title="Website Design", description="Professionelles Website-Design..."
        )
        OfferDetail.objects.create(
            offer=self.offer, title="Basic Design", revisions=2,
            delivery_time_in_days=5, price=100, features=["Logo Design"], offer_type="basic"
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.detail_url = reverse("offer-detail", kwargs={"pk": self.offer.id})


class OfferRetrieveSuccessTests(BaseOfferRetrieveTestCase):
    """Test successful offer retrieval."""

    def setUp(self):
        """Set up and fire GET request."""

        super().setUp()
        self.response = self.client.get(self.detail_url)

    def test_retrieve_offer_returns_200(self):
        """Test that retrieve returns 200 with the correct offer id."""

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.data["id"], self.offer.id)

    def test_retrieve_returns_details(self):
        """Test that retrieve includes the nested detail."""

        self.assertEqual(len(self.response.data["details"]), 1)


class OfferRetrieveAuthenticationTests(BaseOfferRetrieveTestCase):
    """Test that unauthenticated users cannot retrieve an offer."""

    def setUp(self):
        """Set up with cleared credentials and fire GET request."""

        super().setUp()
        self.client.credentials()
        self.response = self.client.get(self.detail_url)

    def test_unauth_user_gets_401(self):
        """Test that unauthenticated request returns 401."""

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OfferRetrieveNotFoundTests(BaseOfferRetrieveTestCase):
    """Test retrieval of a non-existent offer."""

    def setUp(self):
        """Set up and request an unknown offer ID."""

        super().setUp()
        url = reverse("offer-detail", kwargs={"pk": 9999})
        self.response = self.client.get(url)

    def test_offer_not_found_returns_404(self):
        """Test that a non-existent offer returns 404."""

        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)