import stripe
from django.conf import settings

from .base_provider import BasePaymentProvider
from .dto import ProviderPayment

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeProvider(BasePaymentProvider):
    def create_payment(self, payment):
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": f"Booking {payment.booking.id}",
                        },
                        "unit_amount": int(payment.amount * 100),
                    },
                    "quantity": 1,
                }
            ],
            # success_url=settings.STRIPE_SUCCESS_URL,
            # cancel_url=settings.STRIPE_CANCEL_URL,
            success_url=f"http://127.0.0.1:8080/booking_api/payment/success/{payment.booking.id}",
            cancel_url="http://127.0.0.1:8080/booking_api/payment/cancel/",
            metadata={
                "booking_id": payment.booking.id,
            },
        )
        return ProviderPayment(
            payment_id=session.id,
            reference_id=session.payment_intent,
            checkout_url=session.url,
            status=session.status,
        )

    def retrieve_payment(self, provider_payment_id):
        session = stripe.checkout.Session.retrieve(provider_payment_id)
        return ProviderPayment(
            payment_id=session.id,
            reference_id=session.payment_intent,
            checkout_url=session.url,
            status=session.status,
        )

    def get_checkout_url(self, payment):
        return self.retrieve_payment(payment.provider_payment_id).checkout_url
