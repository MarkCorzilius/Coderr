from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token


class BaseOfferRetrieveTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="customer",
        )

        self.offer = Offer.objects.create(
            user=self.user,
            title="Website Design",
            description="Professionelles Website-Design...",
        )

        OfferDetail.objects.create(
            offer=self.offer,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design"],
            offer_type="basic",
        )

        self.client = APIClient()

        self.token = Token.objects.create(
            user=self.user
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        self.detail_url = reverse(
            "offer-detail",
            kwargs={"offer_id": self.offer.id}
        )


class OfferRetrieveSuccessTests(BaseOfferRetrieveTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.detail_url)

    def test_retrieve_offer_returns_200(self):
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.data['id'], self.offer.id)

    def test_retrieve_returns_details(self):
        self.assertEqual(len(self.response.data["details"]), 1)


class OfferRetrieveAuthenticationTests(BaseOfferRetrieveTestCase):
    
    def setUp(self):
        super().setUp()
        self.client.credentials()
        self.response = self.client.get(self.detail_url)

    def test_unauth_user_gets_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OfferRetrieveNotFoundTests(BaseOfferRetrieveTestCase):

    def setUp(self):
        super().setUp()
        url = reverse("offers", kwargs={'offer_id': 9999})
        self.response = self.client.get(url)

    def test_offer_not_found_returns_404(self):
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)