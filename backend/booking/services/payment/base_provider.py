from abc import ABC, abstractmethod


class BasePaymentProvider(ABC):
    @abstractmethod
    def create_payment(self, payment):
        pass

    @abstractmethod
    def retrieve_payment(self, provider_payment_id):
        pass
