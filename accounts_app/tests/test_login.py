from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from accounts_app.models import User
from django.urls import reverse
class LoginTests(APITestCase):

    def setUp(self):
        self.username = "Mark"
        self.password = 'test123'

        self.user = User.objects.create_user(
            username=self.username, 
            email="markcorzilius@gmail.com", 
            password=self.password,  
            type="customer"
        )

        self.client = APIClient()
        self.url = reverse('login') 

    def test_login_success(self):
        data = {
            'username': self.username,
            'password': self.password
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertTrue(len(response.data['token']) > 0)

    def test_login_wrong_password(self):
        data = {
            'username': self.username,
            'password': 'wrongpassword'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_login_wrong_username(self):
        data = {
            'username': 'WrongUsername',
            'password': self.password
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)