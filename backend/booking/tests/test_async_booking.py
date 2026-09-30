import datetime
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from apartments.models.apartments import Apartment
from apartments.models.locations import Locations
from booking.models.booking import Booking
from booking.tasks.booking_complete import complete_finished_bookings
from booking.tasks.expire_booking import cancel_unpaid_booking

User = get_user_model()


class BookingTasksTestCase(APITestCase):
    def setUp(self):
        # Create test data
        self.owner = User.objects.create_user(first_name="owner", email="owner@example.com", password="password123")
        self.client_user = User.objects.create_user(
            first_name="client", email="client@example.com", password="password123"
        )
        self.hacker = User.objects.create_user(first_name="hacker", email="hacker@example.com", password="password123")


        self.test_location = Locations.objects.create(
            name="Test City"
        )


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

    @patch("booking.tasks.booking_complete.complete_booking")
    def test_complete_finished_bookings_task(self, mock_complete_booking):
        """Ensure that completed paid bookings are automatically closed."""
        # Create a booking with a checkout date in the past (yesterday)
        yesterday = timezone.now().date() - timedelta(days=1)
        past_booking = Booking.objects.create(
            user=self.client_user,
            apartment=self.apartment,
            checkin_day=yesterday - timedelta(days=2),
            checkout_day=yesterday,
            status=Booking.STATUS_PAID,
            total_price=100.00,
        )

        complete_finished_bookings()

        mock_complete_booking.assert_called_once_with(booking_id=past_booking.id)

    def test_cancel_unpaid_booking_skips_if_paid(self):
        """The task must NOT cancel a booking if it has already been paid."""
        paid_booking = Booking.objects.create(
            user=self.client_user,
            apartment=self.apartment,
            checkin_day=timezone.now().date(),
            checkout_day=timezone.now().date() + timedelta(days=2),
            status=Booking.STATUS_PAID,
            total_price=100.00,
        )

        with patch("booking.tasks.expire_booking.cancel_booking") as mock_cancel:
            cancel_unpaid_booking(booking_id=paid_booking.id)
            mock_cancel.assert_not_called()

    def test_cancel_unpaid_booking_cancels_if_pending(self):
        """The task must cancel a booking if its status remains PENDING."""
        pending_booking = Booking.objects.create(
            user=self.client_user,
            apartment=self.apartment,
            checkin_day=timezone.now().date(),
            checkout_day=timezone.now().date() + timedelta(days=2),
            status=Booking.STATUS_PENDING,
            total_price=100.00,
        )

        with patch("booking.tasks.expire_booking.cancel_booking") as mock_cancel:
            cancel_unpaid_booking(booking_id=pending_booking.id)
            mock_cancel.assert_called_once_with(booking=pending_booking, reason="payment_timeout")
