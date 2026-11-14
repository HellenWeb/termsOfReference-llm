from unittest.mock import AsyncMock, MagicMock


def make_message(
    user_id: int = 123456789,
    first_name: str = "Артём",
    text: str = "/start",
) -> AsyncMock:
    message = AsyncMock()
    message.from_user = MagicMock(id=user_id, first_name=first_name)
    message.text = text
    message.answer = AsyncMock()
    return message


def make_callback(
    user_id: int = 123456789,
    first_name: str = "Артём",
    data: str = "profile",
) -> AsyncMock:
    callback = AsyncMock()
    callback.from_user = MagicMock(id=user_id, first_name=first_name)
    callback.data = data
    callback.message = AsyncMock()
    callback.answer = AsyncMock()
    return callback
