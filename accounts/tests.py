from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserAuthenticationTest(TestCase):
    def setUp(self):
        self.email = 'test@example.com'
        self.phone_number = '1234567890'
        self.password = 'testpassword'
        self.user = User.objects.create_user(
            email=self.email,
            phone_number=self.phone_number,
            password=self.password
        )

    def test_email_authentication(self):
        # Test authentication using email
        credentials = {
            'username': self.email,
            'password': self.password
        }
        response = self.client.post('/api/auth/login/', credentials)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_phone_number_authentication(self):
        # Test authentication using phone number
        credentials = {
            'username': self.phone_number,
            'password': self.password
        }
        response = self.client.post('/api/auth/login/', credentials)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
