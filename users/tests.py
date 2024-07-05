from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User





class UserRegistrationViewTest(TestCase): # Tests if the URL for the registration view exists.

    def test_registration_view_url_exists_at_desired_location(self):
        response = self.client.get('/users/signup/')
        self.assertEqual(response.status_code, 200)


    def test_registration_view_url_accessible_by_name(self): # Simulates a GET request to the registration URL by name.
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)


    def test_user_registration(self): # Simulates a POST request to register a new user and checks if the user was created successfully.
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'complexpassword',
            'password2': 'complexpassword'
        })
        self.assertEqual(response.status_code, 200)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())


class UserLoginViewTest(TestCase): # Creates a test user for login tests.

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='testuser', password='12345')


    def test_login_view_url_exists_at_desired_location(self): # Tests if the URL for the login view exists.
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)


    def test_login_view_url_accessible_by_name(self):  # Simulates a GET request to the login URL by name.
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)


    def test_user_login(self): # Simulates a POST request to log in a user and checks if the user is authenticated.
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)
