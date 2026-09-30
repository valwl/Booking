from booking.services.booking.booking_failed import mark_booking_payment_failed
from booking.services.booking.booking_paid import mark_booking_as_paid


def handle_stripe_event(event):
    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        booking_id = int(data["metadata"]["booking_id"])
        mark_booking_as_paid(booking_id)

    elif event_type == "checkout.session.expired":
        booking_id = int(data["metadata"]["booking_id"])
        mark_booking_payment_failed(booking_id)
