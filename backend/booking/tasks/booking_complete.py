from celery import shared_task
from django.utils import timezone

from booking.models.booking import Booking
from booking.services.booking.booking_complete import complete_booking


@shared_task
def complete_finished_bookings():
    bookings = Booking.objects.filter(status=Booking.STATUS_PAID, checkout_day__lt=timezone.now().date()).only("id")
    for booking in bookings:
        complete_booking(booking_id=booking.id)
