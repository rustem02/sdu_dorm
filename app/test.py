from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model




User = get_user_model()

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import User
from .serializers import UserRegistrationSerializer

class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')

    def test_registration_without_id_number(self):
        """
        Test the registration endpoint to ensure that a user can be registered
        without providing an id_number.
        """
        data = {
            "email": "pakoc25741@amankro.com",
            "password": "123",
            "password_confirm": "123",
            "first_name": "TEST2",
            "last_name": "USER2",
            "birth_date": "2000-01-01",
            "id_number": "2001421021",
            "faculty": 1,
            "specialty": 6,
            "gender": "Male"

        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(User.objects.get(email='pakoc25741@amankro.com'))

    # def test_registration_with_id_number(self):
    #     """
    #     Test the registration endpoint to ensure that a user can be registered
    #     with an id_number.
    #     """
    #     data = {
    #         'email': 'test2@example.com',
    #         'password': 'verysecure',
    #         'first_remote': 'Jane',
    #         'last_remote': 'Doe',
    #         'birth_date': '1990-02-01',
    #         'id_number': '1234567890'
    #     }
    #     response = self.client.post(self.register_username, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertIsNotNone(User.objects.get(email='test2@example.com'))






class LoginAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='securepassword123')
        self.client = APIClient()
        self.login_url = reverse('api_login')

    def test_user_login_valid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'securepassword123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_user_login_invalid_credentials(self):
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LogoutAPITestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='securepassword123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.logout_url = reverse('logout')

    def test_user_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Successfully logged out.", response.data['detail'])

