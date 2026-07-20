from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from accounts_app.models import User
from offers_app.models import Offer, OfferDetail
from rest_framework.authtoken.models import Token
import copy


class BaseOfferUpdateTestCase(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="business",
        )

        self.user2 = User.objects.create_user(
            username="Tester2",
            email="tester2@gmail.com",
            password="test123",
            type="business",
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

        self.token2 = Token.objects.create(
            user=self.user2
        )

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        self.detail_url = reverse(
            "offer-detail",
            kwargs={"offer_id": self.offer.id}
        )

        self.payload = {
            "title": "Updated Grafikdesign-Paket",
            "description": 'new description',
            "details": [
                {
                    "title": "Basic Design Updated",
                    "revisions": 3,
                    "delivery_time_in_days": 6,
                    "price": 120,
                    "features": [
                        "Logo Design",
                        "Flyer"
                        ],
                        "offer_type": "basic"
                        }
                        ]
                    }


class OfferUpdateSuccessTests(BaseOfferUpdateTestCase):
    
    def setUp(self):
        super().setUp()

    def test_offer_update_returns_200(self):
        response = self.client.patch(self.detail_url, self.payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.offer.user, self.user)

    def test_only_updated_data_changed(self):
        original_title = self.offer.title
        new_payload = copy.deepcopy(self.payload)
        new_payload.pop('title')
        response = self.client.patch(self.detail_url, new_payload)
        self.offer.refresh_from_db()
        offer = Offer.objects.first()
        self.assertEqual(offer.title, original_title)
        self.assertNotEqual(self.offer.description, response.data['description'])


class OfferUpdateAuthorizationTests(BaseOfferUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token2.key}"
        )
        self.response = self.client.patch(self.detail_url, self.payload)

    def test_unauthorized_user_returns_403(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotEqual(self.offer.user, self.user2)


class OfferUpdateNotFoundTests(BaseOfferUpdateTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse(
            "offer-detail",
            kwargs={"offer_id": 9999}
        )
        self.response = self.client.patch(self.url, self.payload)

    def test_not_found_returns_404(self):
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)