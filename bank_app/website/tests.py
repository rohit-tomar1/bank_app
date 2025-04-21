from django.test import TestCase, Client
from django.urls import reverse

from .models.models import Customers  # Assuming you have a Customer model defined
from .utils.cryptography import Cryptography
class LoginViewTestCase(TestCase):
    def setUp(self):
        # Create a test user for login
        encrypted_password = Cryptography.encryption('password123')  # Encrypt the password
        self.user = Customers.objects.create(email='test@example.com', password=encrypted_password)

    def test_get_login_page(self):
        client = Client()
        response = client.get(reverse('login'))  # Assuming 'login' is the URL name for LoginView
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_login_valid_credentials(self):
        client = Client()
        response = client.post(reverse('login'), {'email': 'test@example.com', 'password': 'password123'}, follow=True)
        self.assertEqual(response.status_code, 200)  # Redirect to OTP page
        self.assertEqual(response.redirect_chain[0][0], reverse('otp'))
        # You can add more assertions here to verify session variables and other behavior

    def test_post_login_invalid_email(self):
        client = Client()
        response = client.post(reverse('login'), {'email': 'invalid@example.com', 'password': 'password123'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('Invalid email ID', response.content.decode())

    def test_post_login_invalid_password(self):
        client = Client()
        response = client.post(reverse('login'), {'email': 'test@example.com', 'password': 'invalidpassword'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertIn('Invalid password', response.content.decode())

    # Add more test cases as needed
