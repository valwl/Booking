from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from booking.models.booking import Booking
from booking.services.availability_service import AvailabilityService

channel_layer = get_channel_layer()


def cancel_booking(*, booking, reason: str = "user_cancelled"):
    if booking.status != Booking.STATUS_PENDING:
        return

    booking.status = Booking.STATUS_CANCELLED
    booking.save(update_fields=["status"])

    AvailabilityService.unblock_dates(booking=booking)

    async_to_sync(channel_layer.group_send)(
        f"booking_{booking.id}",
        {
            "type": "booking_event",
            "payload": {
                "type": "booking_cancel",
                "status": "cancelled",
                "reason": reason,
                "booking_id": booking.id,
            },
        },
    )
