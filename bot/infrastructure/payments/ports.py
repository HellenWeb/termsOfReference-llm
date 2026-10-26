from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True, slots=True)
class PaymentCheckout:
    provider_payment_id: str
    confirmation_url: str


class PaymentProvider(Protocol):
    async def create_checkout(self, *, user_id: int, amount: Decimal, credits: int) -> PaymentCheckout: ...

    async def handle_webhook(self, payload: bytes, signature: str | None) -> None: ...
