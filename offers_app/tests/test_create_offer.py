import copy

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail


class BaseOfferTestCase(APITestCase):
    """Shared base payload for offer creation tests."""

    def setUp(self):
        """Set up default offer payload."""

        self.payload = {
            "title": "Frontend-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium",
                },
            ],
        }


class OfferCreateSuccessTests(BaseOfferTestCase):
    """Test successful offer creation by an authenticated business user."""

    def setUp(self):
        """Set up business user and fire POST request."""

        super().setUp()
        self.user = User.objects.create_user(
            username="Tester", email="tester@gmail.com", password="test123", type="business"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("offer-list")
        self.response = self.client.post(self.url, self.payload, format="json")

    def test_create_offer_returns_201(self):
        """Test that creating an offer returns 201 Created."""

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_created_offer_saved_in_db(self):
        """Test that the offer is persisted in the database."""

        offer = Offer.objects.first()
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(offer.title, self.payload["title"])

    def test_offer_details_created(self):
        """Test that all nested offer details are created."""

        offer = Offer.objects.first()
        self.assertEqual(OfferDetail.objects.filter(offer=offer).count(), 3)
        self.assertGreater(len(self.response.data["details"]), 0)

    def test_response_contains_expected_data(self):
        """Test that response contains the submitted title."""

        self.assertEqual(self.payload["title"], self.response.data["title"])


class OfferCreateAuthenticationTests(BaseOfferTestCase):
    """Test that unauthenticated users cannot create offers."""

    def setUp(self):
        """Set up with cleared credentials."""

        super().setUp()
        self.user = User.objects.create_user(
            username="Tester", email="tester@gmail.com", password="test123", type="business"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials()
        self.url = reverse("offer-list")
        self.response = self.client.post(self.url, self.payload, format="json")

    def test_unauth_user_gets_401(self):
        """Test that unauthenticated request returns 401."""

        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OfferCreateAuthorizationTests(BaseOfferTestCase):
    """Test that customer users cannot create offers."""

    def setUp(self):
        """Set up customer user and fire POST request."""

        super().setUp()
        self.user = User.objects.create_user(
            username="Tester", email="tester@gmail.com", password="test123", type="customer"
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("offer-list")
        self.response = self.client.post(self.url, self.payload, format="json")

    def test_customer_access_not_allowed(self):
        """Test that customer user receives 403 Forbidden."""

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)


class OfferCreateValidationTests(BaseOfferTestCase):
    """Test validation errors on offer creation."""

    def setUp(self):
        """Set up business user with a single-detail payload."""

        super().setUp()
        self.user = User.objects.create_user(
            username="Tester", email="tester@gmail.com", password="test123", type="business"
        )
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.url = reverse("offer-list")
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
        self.response = self.client.post(self.url, self.payload, format="json")

    def test_missing_required_field_returns_400(self):
        """Test that missing title field returns 400."""

        payload = self.payload.copy()
        payload.pop("title")
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_invalid_price_returns_400(self):
        """Test that negative price returns 400."""

        payload = copy.deepcopy(self.payload)
        payload["details"][0]["price"] = -100
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class OfferCreateSuccessTests(BaseOfferTestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="business",
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offer-list')
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_create_offer_returns_201(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_created_offer_saved_in_db(self):
        offer = Offer.objects.first()
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(offer.title, self.payload["title"])

    def test_offer_details_created(self):
        offer = Offer.objects.first()
        self.assertEqual(OfferDetail.objects.filter(offer=offer).count(), 3)
        self.assertGreater(len(self.response.data['details']), 0)

    def test_response_contains_expected_data(self):
        self.assertEqual(self.payload['title'], self.response.data['title'])


class OfferCreateAuthenticationTests(BaseOfferTestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="business",
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials()
        self.url = reverse('offer-list')

        self.response = self.client.post(self.url, self.payload, format='json')

    def test_unauth_user_gets_401(self):
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)


class OfferCreateAuthorizationTests(BaseOfferTestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="customer",
        )
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.url = reverse('offer-list')
        self.response = self.client.post(self.url, self.payload, format='json')

    def test_customer_access_not_allowed(self):
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)


class OfferCreateValidationTests(BaseOfferTestCase):

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="business",
        )
        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('offer-list')

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