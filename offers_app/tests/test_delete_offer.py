from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail


class BaseDeleteTestCase(APITestCase):
    """Shared test data for offer delete endpoint tests."""

    def setUp(self):
        """Set up two business users, an offer with details, and tokens."""

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
            offer=self.offer, title="Standard Design", revisions=2,
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


class OfferDeleteSuccessTests(BaseDeleteTestCase):
    """Test successful offer deletion by the offer owner."""

    def setUp(self):
        """Set up and fire DELETE request."""

        super().setUp()
        self.response = self.client.delete(self.detail_url)

    def test_offer_delete_returns_204(self):
        """Test that delete returns 204 No Content."""

        self.assertEqual(self.response.status_code, status.HTTP_204_NO_CONTENT)

    def test_offer_deletes_object(self):
        """Test that offer and its details are removed from the database."""

        self.assertEqual(Offer.objects.count(), 0)
        self.assertEqual(OfferDetail.objects.count(), 0)


class OfferDeleteAuthorizationTests(BaseDeleteTestCase):
    """Test that non-owner cannot delete an offer."""

    def setUp(self):
        """Set up with second user credentials and fire DELETE request."""

        super().setUp()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token2.key}")
        self.response = self.client.delete(self.detail_url)

    def test_unauthorized_user_deletes_offer_returnes_403(self):
        """Test that a non-owner receives 403 Forbidden."""

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.offer.user, self.user2)

    def test_offer_still_exists(self):
        """Test that the offer persists after a failed delete."""

        self.assertEqual(Offer.objects.count(), 1)
        self.assertTrue(Offer.objects.filter(pk=self.offer.pk).exists())


class OfferDeleteNotFoundTests(BaseDeleteTestCase):
    """Test delete on a non-existent offer."""

    def setUp(self):
        """Set up and fire DELETE for an unknown offer ID."""

        super().setUp()
        url = reverse("offer-detail", kwargs={"pk": 9999})
        self.response = self.client.delete(url)

    def test_delete_undefined_offer_returns_404(self):
        """Test that deleting a non-existent offer returns 404."""

        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)