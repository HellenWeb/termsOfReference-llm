from bot.infrastructure.db.models import User


def make_user(
    telegram_id: int = 123456789,
    username: str = "testuser",
    first_name: str = "Артём",
    credits_balance: int = 100,
) -> User:
    return User(
        id=1,
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        credits_balance=credits_balance,
    )
