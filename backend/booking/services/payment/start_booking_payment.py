from django.conf import settings
from django.db import transaction

from booking.models.payment import Payment

from .payment_service import PaymentService


def start_or_get_booking_payment(*, booking):

    with transaction.atomic():
        booking_ref = booking.__class__.objects.select_for_update().get(pk=booking.pk)

        payment = booking_ref.payments.first()

        if payment and payment.provider_payment_id:
            provider_payment = PaymentService.retrieve_payment(payment)

            if provider_payment.status in ["pending", "open"]:
                return provider_payment.checkout_url

        if not payment:
            payment = Payment.objects.create(
                booking=booking_ref, provider=settings.PAYMENT_PROVIDER, amount=booking_ref.total_price
            )

        provider_payment = PaymentService.create_payment(payment)

        payment.provider_payment_id = provider_payment.payment_id
        payment.status = Payment.STATUS_SESSION_CREATED
        payment.provider_reference = provider_payment.checkout_url
        payment.save(update_fields=["provider_payment_id", "provider_reference", "status"])

        return provider_payment.checkout_url
