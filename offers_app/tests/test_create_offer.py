from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from accounts_app.models import User
from offers_app.models import Offer
from rest_framework.authtoken.models import Token
from rest_framework import status
import copy



class OfferCreateSuccessTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="business",
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offers')

        self.payload = {
            "title": "Website Design",
            "description": "Professionelles Website-Design...",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                }
            ],
        }
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_create_offer_returns_201(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_created_offer_saved_in_db(self):
        offer = Offer.objects.first()
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(offer.title, self.payload["title"])

    def test_offer_details_created(self):
        offer = Offer.objects.first()
        self.assertEqual(Offer.objects.filter(offer=offer).count(), 1)
        self.assertGreater(len(self.response.data['details']), 0)

    def test_response_contains_expected_data(self):
        self.assertEqual(self.payload.data['title'], self.response.data['title'])


class OfferCreateAuthenticationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="business",
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials()
        self.url = reverse('offers')

        self.payload = {
            "title": "Website Design",
            "description": "Professionelles Website-Design...",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                }
            ],
        }
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_unauth_user_gets_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OfferCreateAuthorizationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="customer",
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials()
        self.url = reverse('offers')

        self.payload = {
            "title": "Website Design",
            "description": "Professionelles Website-Design...",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                }
            ],
        }
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_customer_access_not_allowed(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)


class OfferCreateValidationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="business",
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offers')

        self.payload = {
            "title": "Website Design",
            "description": "Professionelles Website-Design...",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                }
            ],
        }
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_missing_required_field_returns_400(self):
        payload = self.payload.copy()
        payload.pop('title')
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)


    def test_invalid_price_returns_400(self):
        payload = copy.deepcopy(self.payload)
        payload["details"][0]["price"] = -100

        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)