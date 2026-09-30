import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apartments.models.apartments import Apartment
from apartments.models.locations import Locations
from booking.models.booking import Booking

User = get_user_model()


class BookingAPITestCase(APITestCase):
    def setUp(self):
        # 1. create test data
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

    def test_successful_booking_creation_pending(self):
        """"Ensure a valid request creates a booking with PENDING status."""
        data = {
            "apartment": self.apartment.id,
            "checkin_day": self.start_date.isoformat(),
            "checkout_day": self.end_date.isoformat(),
            "guests": 2,
        }
        response = self.client.post(self.booking_list_url, data, format="json")

        if response.status_code != status.HTTP_201_CREATED:
            print("\n!!! СЕРИАЛИЗАТОР ВЕРНУЛ ОШИБКУ:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        booking = Booking.objects.first()
        self.assertEqual(booking.status, "pending")
        self.assertEqual(booking.user, self.client_user)

    def test_double_booking_protection(self):
        """Ensure booking overlapping dates returns a 400 Bad Request error."""
        # Create an initial booking via domain service to lock dates in AvailabilityService
        from booking.services.booking.booking_create import create_booking

        create_booking(user=self.client_user, apartment=self.apartment, checkin=self.start_date, checkout=self.end_date)

        data = {
            "apartment": self.apartment.id,
            "checkin_day": self.start_date.isoformat(),
            "checkout_day": self.end_date.isoformat(),
            "guests": 2,
        }

        response = self.client.post(self.booking_list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_dates_validation(self):
        """Ensure date validation fails if checkout day is prior to checkin day."""
        data = {
            "apartment": self.apartment.id,
            "checkin_day": self.end_date.isoformat(),
            "checkout_day": self.start_date.isoformat(),
            "guests": 2,
        }
        response = self.client.post(self.booking_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_available_dates_endpoint(self):
        """Ensure the available dates endpoint returns currently blocked slots."""
        Booking.objects.create(
            user=self.client_user,
            apartment=self.apartment,
            checkin_day=self.start_date,
            checkout_day=self.end_date,
            status="PAID",
            total_price=Decimal("300.00"),
        )
        response = self.client.get(self.available_dates_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(str(self.start_date), str(response.data))
