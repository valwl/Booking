from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from . base import BaseAuthTestCase

User = get_user_model()


class AuthAPIViewsTestCase(BaseAuthTestCase):
    """API functional tests targeting registration, login, logout, and profile management endpoints."""

    @patch("users.services.auth_service.AuthService.register")
    @patch("users.services.token_service.TokenService.issue_tokens_for_user")
    def test_api_registration_success(self, mock_issue_tokens, mock_register):
        """Ensure the registration endpoint successfully persists a user and returns authentication tokens."""
        new_user = User(email="new@example.com", first_name="A", last_name="B")
        mock_register.return_value = new_user
        mock_issue_tokens.return_value = self.fake_tokens

        data = {
            "email": "new@example.com",
            "phone_number": "89992223344",
            "password": "newpassword123",
            "first_name": "A",
            "last_name": "B",
        }
        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("tokens", response.data)
        self.assertIn("user", response.data)
        self.assertEqual(response.data["tokens"]["access"], "fake_access_token")

    @patch("users.services.auth_service.AuthService.login")
    @patch("users.services.token_service.TokenService.issue_tokens_for_user")
    def test_api_login_success(self, mock_issue_tokens, mock_login):
        """Ensure the login endpoint issues valid authorization tokens upon receiving valid credentials."""
        mock_login.return_value = self.user
        mock_issue_tokens.return_value = self.fake_tokens

        data = {"username": "test_user@example.com", "password": self.password}
        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["tokens"]["access"], "fake_access_token")

    @patch("users.services.token_service.TokenService.blacklist")
    def test_api_logout(self, mock_blacklist):
        """Verify that an authenticated user can successfully log out by blacklisting their refresh token."""
        self.client.force_authenticate(user=self.user)

        data = {"refresh": "token_to_blacklist"}
        response = self.client.post(self.logout_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_blacklist.assert_called_once_with("token_to_blacklist")

    def test_api_logout_unauthorized(self):
        """Ensure an unauthenticated logout request is rejected with a 401 Unauthorized status."""
        response = self.client.post(self.logout_url, {"refresh": "token"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_profile(self):
        """Verify the 'user/me/' endpoint correctly retrieves the profile data of the currently authenticated user."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    @patch("users.services.user_service.UserService.change_user_password")
    def test_password_change(self, mock_change_password):
        """Verify that an authenticated user can successfully update their password profile."""
        self.client.force_authenticate(user=self.user)

        data = {"old_password": self.password, "new_password": "brand_new_password_123"}
        response = self.client.post(self.password_change_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        mock_change_password.assert_called_once_with(user=self.user, new_password="brand_new_password_123")

