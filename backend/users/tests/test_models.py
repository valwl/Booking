from django.contrib.auth import get_user_model
from django.urls import reverse
from . base import BaseAuthTestCase

User = get_user_model()


class UserModelTestCase(BaseAuthTestCase):
    """Unit tests targeting CustomUser data constraints and phone number normalization."""

    def test_phone_normalization(self):
        """Ensure valid Russian mobile strings are standard-formatted by the manager."""
        normalized_11 = User.objects.phone_normalise("89991112233")
        self.assertEqual(normalized_11, "+7 (999) 111-22-33")

        normalized_10 = User.objects.phone_normalise("9991112233")
        self.assertEqual(normalized_10, "+7 (999) 111-22-33")

        self.assertIsNone(User.objects.phone_normalise("123"))

    def test_create_user_without_credentials_raises_error(self):
        """Verify the manager drops a ValueError if both email and phone fields are omitted."""
        with self.assertRaises(ValueError):
            User.objects.create_user(password="123")
