from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts_app.models import User
from rest_framework.authtoken.models import Token

class RegisterTests(APITestCase):
    
    def setUp(self):
        self.password = '@test123'

        self.user = User.objects.create_user(username="Mark", email="markcorzilius@gmail.com", password=self.password, type="customer")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('register')

    def test_register_success(self):
        self.data = {
            'username': 'Valeria',
            'email': 'valeria@gmail.com',
            'password': self.password,
            'repeated_password': self.password,
            'type': 'customer'
        }       
        response = self.client.post(self.url, self.data, format='json')
        print('response test: ', response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='valeria@gmail.com').exists())

    def test_register_password_mismatch(self):
        data = {
            'username': 'Valeria',
            'email': 'valeria@gmail.com',
            'password': self.password,
            'repeated_password': 'wrongPassword123',
            'type': 'customer'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(email='valeria@gmail.com').exists())

    def test_register_duplicate_email(self):
        data = {
            'username': 'AnotherName',
            'email': self.user.email,
            'password': self.password,
            'repeated_password': self.password,
            'type': 'customer'
            }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.filter(email=data['email']).count(), 1)