from booking.models.payment import Payment

from .provider_factory import PaymentProviderFactory


class PaymentService:
    @staticmethod
    def create_payment(payment):
        provider = PaymentProviderFactory.get_provider()

        provider_result = provider.create_payment(payment)
        payment.provider_payment_id = provider_result.payment_id
        payment.provider_reference = provider_result.reference_id
        payment.status = Payment.STATUS_SESSION_CREATED
        payment.save(
            update_fields=[
                "provider_payment_id",
                "provider_reference",
                "status",
            ]
        )
        return provider_result

    @staticmethod
    def retrieve_payment(payment):
        provider = PaymentProviderFactory.get_provider()

        return provider.retrieve_payment(payment.provider_payment_id)
