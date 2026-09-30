from django.conf import settings

from .stripe_provider import StripeProvider
from .youmany_provider import YooMoneyProvider


class PaymentProviderFactory:
    providers = {
        "stripe": StripeProvider(),
        "yoomoney": YooMoneyProvider(),
    }

    @classmethod
    def get_provider(cls):
        provider_name = settings.PAYMENT_PROVIDER
        return cls.providers[provider_name]
