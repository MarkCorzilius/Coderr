from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts_app.models import User
from rest_framework.authtoken.models import Token

class AccountTests(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username="Mark", email="markcorzilius@gmail.com", password="test123", repeated_password="test123", type="customer")

        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('register')

    def test_register_success(self):
        self.data = {
            'username': 'Valeria',
            'email': 'valeria@gmail.com',
            'password': 'test123',
            'repeated_password': 'test123',
            'type': 'customer'
        }       
        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='valeria@gmail.com').exists())

    def test_register_password_mismatch(self):
        data = {
            'username': 'Valeria',
            'email': 'valeria@gmail.com',
            'password': 'test123',
            'repeated_password': 'wrong123',
            'type': 'customer'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email='valeria@gmail.com').exists())

    def test_register_duplicate_email(self):
        data = {
            'username': 'AnotherName',
            'email': self.user.email,
            'password': self.user.password,
            'repeated_password': self.user.password,
            'type': 'customer'
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email=data['email']).count(), 1)

    def test_register_duplicate_username(self):
        data = {
            'username': self.user.username,
            'email': 'good@gmail.com',
            'password': self.user.password,
            'repeated_password': self.user.password,
            'type': 'customer'
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(username=data['username']).count(), 1)
