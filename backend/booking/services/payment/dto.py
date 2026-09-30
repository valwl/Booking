from dataclasses import dataclass


@dataclass
class ProviderPayment:
    payment_id: str
    reference_id: str | None
    checkout_url: str
    status: str
