from django.db import transaction

from booking.models.payment import Payment
from booking.services.booking.booking_failed import mark_booking_payment_failed
from booking.services.booking.booking_paid import mark_booking_as_paid


@transaction.atomic
def handle_yoomoney_event(payload):
    event_type = payload.get("event")
    payment_object = payload.get("object", {})
    provider_payment_id = payment_object.get("id")
    if not provider_payment_id:
        return

    payment = Payment.objects.select_for_update().filter(provider_payment_id=provider_payment_id).first()

    if not payment:
        return
    booking = payment.booking
    if event_type == "payment.succeeded" and payment.status != Payment.STATUS_PAID:
        payment.status = Payment.STATUS_PAID
        payment.save(update_fields=["status"])
        mark_booking_as_paid(booking.id)
    elif event_type == "payment.canceled" and payment.status != Payment.STATUS_FAILED:
        payment.status = Payment.STATUS_FAILED
        payment.save(update_fields=["status"])
        mark_booking_payment_failed(booking.id)
