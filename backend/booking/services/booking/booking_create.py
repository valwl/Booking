from django.conf import settings
from django.db import transaction

from apartments.models.apartments import Apartment
from booking.models.booking import Booking
from booking.services.booking.pricing_calculate import calculate_booking_price
from booking.tasks.expire_booking import cancel_unpaid_booking

from ..availability_service import AvailabilityService


@transaction.atomic
def create_booking(*, user, apartment, checkin, checkout):
    apartment_locked = Apartment.objects.select_for_update().get(id=apartment.id)
    availability = AvailabilityService()
    if not availability.is_available(apartment=apartment, checkin=checkin, checkout=checkout):
        raise ValueError("Appartment not available")

    price = calculate_booking_price(
        apartment=apartment_locked,
        checkin=checkin,
        checkout=checkout,
    )

    booking = Booking.objects.create(
        user=user,
        apartment=apartment,
        checkin_day=checkin,
        checkout_day=checkout,
        total_price=price,
        status=Booking.STATUS_PENDING,
    )

    availability.block_dates(booking=booking)
    transaction.on_commit(
        lambda: cancel_unpaid_booking.apply_async(args=(booking.id,), countdown=settings.BOOKING_PAYMENT_TIMEOUT)
    )
    return booking
