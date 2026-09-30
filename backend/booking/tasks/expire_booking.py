import logging

from celery import shared_task

from booking.models.booking import Booking
from booking.selectors.booking_selectors import get_booking_by_id
from booking.services.booking.booking_cancel import cancel_booking

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def cancel_unpaid_booking(self, booking_id):
    booking = get_booking_by_id(booking_id)

    logger.info(f"Celery task running for booking {booking_id}, status={booking.status}")

    if booking.status == Booking.STATUS_PAID:
        logger.info("Booking already paid. Skipping")
        return

    cancel_booking(booking=booking, reason="payment_timeout")
    logger.info(f"Booking cancelled: {booking.id}")
