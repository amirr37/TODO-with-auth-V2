import rest_framework.status
from django.test import TestCase, Client
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from account_module.models import CustomUser
from account_module.views import SignupView
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from account_module.models import CustomUser
from account_module.views import LoginView
from account_module.forms import LoginForm


# Create your tests here.


class SignupViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user_data = {
            'username': self.username,
            'email': 'test@example.com',
            'password': self.password,
            'confirm_password': self.password,
        }

    def test_get_signup_view(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/signup.html')

    def test_post_signup_view_with_valid_data(self):
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirect response
        self.assertRedirects(response, self.login_url)
        # Check if the user is created in the database
        User = get_user_model()
        self.assertTrue(User.objects.filter(username=self.username).exists())

    def test_post_signup_view_with_existing_username(self):
        # Create a user with the same username as the one we'll try to sign up with
        User = get_user_model()
        User.objects.create_user(username=self.username, password=self.password)
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/signup.html')
        self.assertFormError(response, 'signup_form', 'username', 'Username already exists')

    def test_post_signup_view_with_not_same_password_and_confirm_password(self):
        """
        Test signup view with mismatched password and confirm password.
        """
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'confirm_password': 'differentpassword',
        }

        response = self.client.post(self.signup_url, data=user_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/signup.html')
        self.assertFormError(response, 'signup_form', 'confirm_password', 'Passwords do not match.')

    def test_post_signup_view_with_invalid_email(self):
        user_data = {
            'username': 'testuser',
            'email': 'test.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword',
        }

        response = self.client.post(self.signup_url, data=user_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/signup.html')
        self.assertFormError(response, 'signup_form', 'email', 'Enter a valid email address.')


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)

    def test_get_login_view(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/login.html')
        self.assertIsInstance(response.context['login_form'](), LoginForm)

    def test_post_login_view_with_valid_credentials(self):
        login_data = {'username': self.username, 'password': self.password}

        response = self.client.post(self.login_url, data=login_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_module/index_page.html')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_post_login_view_with_invalid_credentials(self):
        """test fails"""
        # todo : fix the bug
        login_data = {'username': self.username, 'password': 'wrong_password'}

        response = self.client.post(self.login_url, data=login_data, )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/login.html')
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertFormError(response, 'login_form', 'username', 'wrong username or password')
