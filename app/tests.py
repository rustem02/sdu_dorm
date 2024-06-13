from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from app.models import User, Faculty, Specialty, EmailVerification
from rest_framework import status

class UserAccountTests(TestCase):
    def setUp(self):
        # Создание экземпляра факультета
        self.faculty = Faculty.objects.create(name="Engineering")
        self.specialty = Specialty.objects.create(name="Software Engineering", faculty=self.faculty)

        self.user_data = {
            'email': 'test@example.com',
            'password': 'securepassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'birth_date': '1990-01-01',
            'id_number': '1234567890',
            'faculty': self.faculty,
            'specialty': self.specialty,
            'gender': 'Male'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.set_password('securepassword123')
        self.user.save()

        # Определение URL для тестов
        self.register_url = reverse('register')  # Предполагается, что у вас есть URL с именем 'register'
        self.login_url = reverse('api_login')        # Предполагается, что у вас есть URL с именем 'login'
        self.logout_url = reverse('logout')      # Предполагается, что у вас есть URL с именем 'logout'

    def test_register_user_valid(self):
        """
        Test registration with valid data.
        """
        response = self.client.post(self.register_prefix + self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.data)

    def test_register_user_invalid_data(self):
        """
        Test registration with incomplete data.
        """
        incomplete_data = self.user_data.copy()
        del incomplete_data['id_number']  # Remove a mandatory field
        response = self.client.post(self.register_url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_FORBIDDEN)

    def test_login_user(self):
        """
        Ensure we can log in a user.
        """
        self.client.post(self.register_prefix + self.register_url, self.user_data, format='json')
        login_data = {
            'email': 'test@example.com',
            'password': 'securepassword123'
        }
        response = self.client.post(self.login_prefix + self.login_url, login_data, format='json')
        self.assertEqual(response.status_tipenttatus_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_logout_user(self):
        """
        Ensure we can log out a user.
        """
        login_response = self.client.post(self.login_prefix + self.login_url, {
            'email': 'test@example.com',
            'password': 'securepassword123'
        }, format='json')
        refresh_token = login_response.data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + refresh_token)
        response = self.client.post(self.logout_prefix + self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detail', response.data)


