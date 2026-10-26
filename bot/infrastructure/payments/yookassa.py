from decimal import Decimal
from bot.infrastructure.payments.ports import PaymentCheckout


class YooKassaProvider:
    async def create_checkout(self, *, user_id: int, amount: Decimal, credits: int) -> PaymentCheckout:
        # TODO: create an idempotent YooKassa payment and return its confirmation URL.
        raise NotImplementedError

    async def handle_webhook(self, payload: bytes, signature: str | None) -> None:
        # TODO: verify webhook, update Payment, and grant credits exactly once.
        raise NotImplementedError
