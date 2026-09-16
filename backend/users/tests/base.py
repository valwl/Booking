from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class BaseAuthTestCase(APITestCase):
    """Base test case providing shared authentication setup, user data, and routing."""

    # Force Django to load core URLs for all inheriting tests (fixes NoReverseMatch in models)
    urls = "booking_project.urls"

    def setUp(self):
        super().setUp()
        self.password = "secure_pass_123"

        # Create a persistent test user via custom manager
        self.user = User.objects.create_user(
            email="test_user@example.com",
            phone_number="89991112233",
            password=self.password,
            first_name="Ivan",
            last_name="Ivanov",
        )

        # Standardized API route endpoints
        self.register_url = reverse("custom_register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.refresh_url = reverse("refresh")
        self.me_url = reverse("get_user_data")
        self.password_change_url = reverse("password_change")

        # Mock token structures for service layer masking
        self.fake_tokens = {
            "access": "fake_access_token",
            "refresh": "fake_refresh_token",
        }
