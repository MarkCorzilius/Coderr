from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from accounts_app.models import User
from offers_app.models import Offer, OfferDetail


class BaseOffersTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="customer",
        )

        self.offer1 = Offer.objects.create(
            user=self.user,
            title="Website Design",
            description="Professionelles Website-Design...",
        )

        self.offer2 = Offer.objects.create(
            user=self.user,
            title="Backend Tests",
            description="Testing backend...",
        )

        OfferDetail.objects.create(
            offer=self.offer1,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic",
        )

        OfferDetail.objects.create(
            offer=self.offer1,
            title="Standard Design",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=["Logo Design", "Visitenkarte", "Briefpapier"],
            offer_type="standard",
        )

        OfferDetail.objects.create(
            offer=self.offer1,
            title="Premium Design",
            revisions=10,
            delivery_time_in_days=10,
            price=500,
            features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            offer_type="premium",
        )

        OfferDetail.objects.create(
            offer=self.offer2,
            title="Basic Design",
            revisions=2,
            delivery_time_in_days=5,
            price=100,
            features=["Logo Design", "Visitenkarte"],
            offer_type="basic",
        )

        OfferDetail.objects.create(
            offer=self.offer2,
            title="Standard Design",
            revisions=5,
            delivery_time_in_days=7,
            price=200,
            features=["Logo Design", "Visitenkarte", "Briefpapier"],
            offer_type="standard",
        )

        OfferDetail.objects.create(
            offer=self.offer2,
            title="Premium Design",
            revisions=10,
            delivery_time_in_days=10,
            price=500,
            features=["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            offer_type="premium",
        )

        self.client = APIClient()
        self.url = reverse("offer-list")


class OfferListSuccessTests(BaseOffersTestCase):

    def test_get_list_returns_200(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_list_returns_all_offers(self):
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_list_returns_expected_offers(self):
        response = self.client.get(self.url)

        titles = [offer["title"] for offer in response.data['results']]

        self.assertIn(self.offer1.title, titles)
        self.assertIn(self.offer2.title, titles)


class OfferListFilterTests(BaseOffersTestCase):

    def test_filter_by_creator(self):
        response = self.client.get(
            self.url,
            {"creator_id": self.user.id},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        for offer in response.data['results']:
            self.assertEqual(offer['user'], self.user.id)


class OfferListSearchTests(BaseOffersTestCase):

    def test_search_by_title(self):
        response = self.client.get(
            self.url,
            {"search": "Websit"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(
            response.data['results'][0]["title"],
            self.offer1.title,
        )

    def test_search_returns_empty_result(self):
        response = self.client.get(
            self.url,
            {"search": "SomethingThatDoesNotExist"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)


class OfferListValidationTests(BaseOffersTestCase):

    def test_filter_returns_empty_result(self):
        response = self.client.get(
            self.url,
            {"creator_id": 999999},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_returns_empty_list_when_no_offers_exist(self):
        Offer.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])


class OfferListPaginationTests(BaseOffersTestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="Tester",
            email="tester@gmail.com",
            password="test123",
            type="customer",
        )

        for i in range(15):
            Offer.objects.create(
                user=self.user,
                title=f"Offer {i}",
                description="Test",
            )

        self.client = APIClient()
        self.url = reverse("offer-list")

    def test_pagination_returns_first_page(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 15)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])

    def test_pagination_returns_second_page(self):
        response = self.client.get(
            self.url,
            {"page": 2},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNone(response.data["next"])

    def test_page_out_of_range(self):
        response = self.client.get(
            self.url,
            {"page": 3},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )