"""Тесты хендлера профиля."""
from bot.handlers.profile import profile_callback_handler, profile_handler


async def test_profile_handler_sends_html_text(fake_message, fake_user):
    await profile_handler(fake_message, fake_user)

    fake_message.answer.assert_awaited_once()
    args, kwargs = fake_message.answer.await_args
    assert kwargs["parse_mode"] == "HTML"
    assert "👤 <b>Профиль</b>" in args[0]
    assert f"💳 Кредитов: <b>{fake_user.credits_balance}</b>" in args[0]


async def test_profile_callback_edits_message(fake_callback, fake_user):
    await profile_callback_handler(fake_callback, fake_user)

    fake_callback.message.edit_text.assert_awaited_once()
    args, kwargs = fake_callback.message.edit_text.await_args
    assert kwargs["parse_mode"] == "HTML"
    assert f"Привет, {fake_callback.from_user.first_name}!" in args[0]
    fake_callback.answer.assert_awaited_once()
