import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apartments.models.apartments import Apartment
from apartments.models.locations import Locations
from booking.models.booking import Booking
from booking.models.payment import Payment

User = get_user_model()


class BookingWebhooksTestCase(APITestCase):
    def setUp(self):
        # Create test data
        self.owner = User.objects.create_user(first_name="owner", email="owner@example.com", password="password123")
        self.client_user = User.objects.create_user(
            first_name="client", email="client@example.com", password="password123"
        )
        self.hacker = User.objects.create_user(first_name="hacker", email="hacker@example.com", password="password123")


        self.test_location = Locations.objects.create(name="Test City")


        self.apartment = Apartment.objects.create(
            title="Luxury Test Apartment",
            description="Beautiful views, production-ready quality.",
            user=self.owner,
            base_price=Decimal("100.00"),
            weekend_price=Decimal("150.00"),
            location=self.test_location,
        )


        self.start_date = datetime.date.today() + datetime.timedelta(days=2)
        self.end_date = datetime.date.today() + datetime.timedelta(days=5)


        self.booking_list_url = reverse("booking-list")
        self.stripe_webhook_url = reverse("stripe_webhook")
        self.available_dates_url = reverse("available_dates", kwargs={"apartment_id": self.apartment.id})

        # Authenticate the honest client by default for REST test cases
        self.client.force_authenticate(user=self.client_user)

    def test_stripe_webhook_updates_status_and_idempotency(self):
        """Simulate Stripe webhook: verify state transition to PAID and ensure processing is idempotent."""
        booking = Booking.objects.create(
            user=self.client_user,
            apartment=self.apartment,
            checkin_day=self.start_date,
            checkout_day=self.end_date,
            status=Booking.STATUS_PENDING,
            total_price=Decimal("300.00"),
        )
        stripe_session_id = "cs_test_abc123"
        Payment.objects.create(
            booking=booking,
            provider="stripe",
            amount=booking.total_price,
            provider_payment_id=stripe_session_id,
            status=Payment.STATUS_SESSION_CREATED,
        )

        stripe_payload = {
            "id": "evt_test_webhook",
            "object": "event",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": stripe_session_id,
                    "payment_status": "paid",
                    "metadata": {"booking_id": str(booking.id)},
                }
            },
        }


        self.client.logout()


        response1 = self.client.post(self.stripe_webhook_url, stripe_payload, format="json")
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        booking.refresh_from_db()
        self.assertEqual(booking.status, "paid")


        response2 = self.client.post(self.stripe_webhook_url, stripe_payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        booking.refresh_from_db()
        self.assertEqual(booking.status, "paid")
