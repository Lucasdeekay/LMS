from unittest.mock import patch

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from App.models import CustomUser


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')  # Assuming the URL name for HomeView is 'home'

    def test_home_view_status_code(self):
        """Test that the home view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """Test that the home view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'app/home.html')


class AboutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('about')  # Assuming the URL name for AboutView is 'about'

    def test_about_view_status_code(self):
        """Test that the about view returns a 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_about_view_template(self):
        """Test that the about view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'app/about.html')


class ContactViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('contact')  # Assuming the URL name for ContactView is 'contact'

    def test_contact_view_get_request(self):
        """Test that the contact view handles GET request correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/contact.html')

    def test_contact_view_post_request_missing_fields(self):
        """Test POST request with missing fields shows an error message."""
        response = self.client.post(self.url, data={
            'name': '',  # Missing name
            'email': '',  # Missing email
            'message': ''  # Missing message
        })

        # Check that the form renders again with an error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/contact.html')

        # Verify that an error message is added to the context
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("All fields are required." in str(message) for message in messages))

    def test_contact_view_post_request_success(self):
        """Test POST request with all fields provided shows a success message."""
        response = self.client.post(self.url, data={
            'name': 'Dennis',
            'email': 'dennis@example.com',
            'message': 'This is a test message.'
        })

        # Check that the form renders again with a success message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/contact.html')

        # Verify that a success message is added to the context
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Thank you for contacting us." in str(message) for message in messages))


class RegistrationViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')  # Assuming the URL name for RegistrationView is 'register'
        # Creating a user for testing username and email uniqueness
        self.existing_user = CustomUser.objects.create_user(
            username='existinguser', email='existing@example.com', password='password123'
        )

    def test_registration_view_get_request(self):
        """Test that the registration view handles GET request correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/register.html')

    def test_registration_post_password_mismatch(self):
        """Test that a password mismatch results in an error message."""
        response = self.client.post(self.url, data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password456'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/register.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Passwords do not match." in str(message) for message in messages))

    def test_registration_post_username_exists(self):
        """Test that submitting an existing username results in an error message."""
        response = self.client.post(self.url, data={
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/register.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Username already taken." in str(message) for message in messages))

    def test_registration_post_email_exists(self):
        """Test that submitting an existing email results in an error message."""
        response = self.client.post(self.url, data={
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/register.html')

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Email already registered." in str(message) for message in messages))

    def test_registration_post_success(self):
        """Test a successful registration."""
        response = self.client.post(self.url, data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })

        # Check if the response is a redirect to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Verify that the user was created in the database
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

        # Verify that a success message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Registration successful. You can log in now." in str(message) for message in messages))


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')  # Assuming the URL name for LoginView is 'login'
        # Create a user for login tests
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@example.com', password='password123'
        )

    def test_login_view_get_request(self):
        """Test that the login view handles GET request correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/login.html')

    def test_login_view_post_invalid_credentials(self):
        """Test login with invalid credentials results in an error message."""
        response = self.client.post(self.url, data={
            'username': 'wronguser',
            'password': 'wrongpassword'
        })

        # Check that the login page is rendered again with an error message
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/login.html')

        # Verify that the error message is added to the context
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Invalid username or password." in str(message) for message in messages))

    def test_login_view_post_success(self):
        """Test login with valid credentials."""
        response = self.client.post(self.url, data={
            'username': 'testuser',
            'password': 'password123'
        })

        # Check if the response is a redirect to the dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

        # Verify that the user is authenticated
        user = authenticate(username='testuser', password='password123')
        self.assertIsNotNone(user)

        # Verify that the success message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Login successful." in str(message) for message in messages))



class ForgotPasswordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('forgot_password')  # Assuming the URL name for ForgotPasswordView is 'forgot_password'

        # Create a user for testing
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123'
        )

    def test_forgot_password_view_get_request(self):
        """Test that the forgot password view handles GET request correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/forgot_password.html')

    def test_forgot_password_post_unregistered_email(self):
        """Test that submitting an unregistered email results in an error message."""
        response = self.client.post(self.url, data={'email': 'unregistered@example.com'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/forgot_password.html')

        # Verify that an error message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Email not registered." in str(message) for message in messages))

    @patch('App.views.send_mail')
    def test_forgot_password_post_registered_email(self, mock_send_mail):
        """Test that submitting a registered email sends a password reset email."""
        response = self.client.post(self.url, data={'email': 'testuser@example.com'})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/forgot_password.html')

        # Verify that the success message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Password reset link has been sent to your email." in str(message) for message in messages))

        # Verify that the email was sent
        mock_send_mail.assert_called_once()

        # Verify the token generation and URL encoding
        user = CustomUser.objects.get(email='testuser@example.com')
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Check if the URL contains the correct uid and token
        reset_url = response.context['reset_url']
        self.assertIn(uid, reset_url)
        self.assertIn(token, reset_url)


class PasswordResetViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='old_password123'
        )
        # Generate the reset link
        self.token = default_token_generator.make_token(self.user)
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.url = reverse('reset_password', kwargs={'uidb64': self.uidb64, 'token': self.token})

    def test_password_reset_get_request_valid_link(self):
        """Test that a valid password reset link renders the reset password page with 'valid' flag."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/reset_password.html')
        self.assertTrue(response.context['valid'])

    def test_password_reset_get_request_invalid_link(self):
        """Test that an invalid password reset link renders the reset password page with 'invalid' flag."""
        invalid_token = 'invalid_token'
        invalid_url = reverse('reset_password', kwargs={'uidb64': self.uidb64, 'token': invalid_token})

        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/reset_password.html')
        self.assertFalse(response.context['valid'])

        # Check if the error message is shown
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Invalid link." in str(message) for message in messages))

    def test_password_reset_post_password_mismatch(self):
        """Test that if passwords do not match, an error message is displayed."""
        response = self.client.post(self.url, data={
            'password': 'new_password123',
            'confirm_password': 'different_password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/reset_password.html')
        self.assertTrue(response.context['valid'])

        # Verify that the error message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Passwords do not match." in str(message) for message in messages))

    @patch('App.views.send_mail')  # Mocking email sending
    def test_password_reset_post_success(self, mock_send_mail):
        """Test a successful password reset."""
        response = self.client.post(self.url, data={
            'password': 'new_password123',
            'confirm_password': 'new_password123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Verify that the user's password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password123'))

        # Verify that the success message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Password has been reset. You can log in now." in str(message) for message in messages))

    def test_password_reset_post_user_not_found(self):
        """Test that if the user is not found, an error message is displayed."""
        invalid_uidb64 = urlsafe_base64_encode(force_bytes(6763787))
        invalid_token = 'invalid_token'
        invalid_url = reverse('reset_password', kwargs={'uidb64': invalid_uidb64, 'token': invalid_token})

        response = self.client.post(invalid_url, data={
            'password': 'new_password123',
            'confirm_password': 'new_password123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

        # Check if the error message is shown
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("User not found." in str(message) for message in messages))


class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('change_password')  # Assuming the URL name for ChangePasswordView is 'change_password'
        # Create a user and log them in for testing password change
        self.user = CustomUser.objects.create_user(
            username='testuser', email='testuser@example.com', password='old_password123'
        )
        self.client.login(username='testuser', password='old_password123')

    def test_change_password_view_get_request(self):
        """Test that the change password view handles GET request correctly."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/change_password.html')

    def test_change_password_post_password_mismatch(self):
        """Test that a password mismatch results in an error message."""
        response = self.client.post(self.url, data={
            'old_password': 'old_password123',
            'new_password': 'new_password123',
            'confirm_password': 'different_password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/change_password.html')

        # Verify that an error message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Passwords do not match." in str(message) for message in messages))

    def test_change_password_post_incorrect_old_password(self):
        """Test that an incorrect old password results in an error message."""
        response = self.client.post(self.url, data={
            'old_password': 'wrong_password',
            'new_password': 'new_password123',
            'confirm_password': 'new_password123'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app/change_password.html')

        # Verify that an error message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Old password is incorrect." in str(message) for message in messages))

    def test_change_password_post_success(self):
        """Test successful password change."""
        response = self.client.post(self.url, data={
            'old_password': 'old_password123',
            'new_password': 'new_password123',
            'confirm_password': 'new_password123'
        })

        # Check if the response is a redirect to the dashboard
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

        # Verify that the user's password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password123'))

        # Verify that the success message is added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Password changed successfully." in str(message) for message in messages))
