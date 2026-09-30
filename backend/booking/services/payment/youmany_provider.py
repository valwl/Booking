import uuid

from django.conf import settings
from yookassa import Configuration
from yookassa import Payment as YooKasaPayment

from .base_provider import BasePaymentProvider
from .dto import ProviderPayment

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class YooMoneyProvider(BasePaymentProvider):
    def create_payment(self, payment):
        payment_object = YooKasaPayment.create(
            {
                "amount": {"value": str(payment.amount), "currency": "RUB"},
                "capture": True,
                "confirmation": {
                    "type": "redirect",
                    "return_url": settings.PAYMENT_RETURN_URL,
                },
                "description": f"Booking {payment.booking.id}",
                "metadata": {"booking_id": str(payment.booking.id)},
            },
            str(uuid.uuid4()),
        )
        return ProviderPayment(
            payment_id=payment_object.id,
            reference_id=None,
            checkout_url=(payment_object.confirmation.confirmation_url),
            status=payment_object.status,
        )

    def retrieve_payment(self, provider_payment_id):
        payment_object = YooKasaPayment.find_one(provider_payment_id)

        checkout_url = None
        if payment_object.confirmation and hasattr(payment_object.confirmation, "confirmation_url"):
            checkout_url = payment_object.confirmation.confirmation_url

        return ProviderPayment(
            payment_id=payment_object.id,
            reference_id=None,
            checkout_url=checkout_url,
            status=payment_object.status,
        )
