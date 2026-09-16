from django.contrib.auth import authenticate, get_user_model
from django.urls import reverse
from . base import BaseAuthTestCase

User = get_user_model()


class AuthBackendTestCase(BaseAuthTestCase):
    """Integration tests verifying CustomAuthBackend authentication strategies."""

    def test_authenticate_by_email_success(self):
        """Verify successful user authentication via CustomAuthBackend using an email address."""
        user = authenticate(username="test_user@example.com", password=self.password)
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)

    def test_authenticate_by_phone_success(self):
        """Ensure the backend normalizes raw phone input strings and successfully authenticates the user."""
        # Pass a raw phone string — the backend must normalize it internally to match the user record
        user = authenticate(username="89991112233", password=self.password)
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)

    def test_authenticate_fail(self):
        """Verify that authenticate returns None given invalid credentials or non-existent usernames."""
        user_wrong_pass = authenticate(username="test_user@example.com", password="wrong_password")
        self.assertIsNone(user_wrong_pass)

        user_not_found = authenticate(username="unknown@example.com", password=self.password)
        self.assertIsNone(user_not_found)


