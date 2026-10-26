from aiogram import Router
from aiogram.types import Message

from bot.application.generations import GenerationService

router = Router(name=__name__)


def get_generation_service() -> GenerationService:
    """Build the use case from application dependencies.

    TODO: replace with container/middleware-provided dependencies.
    """
    raise NotImplementedError("Configure repositories and queue in the application container")


@router.message()
async def submit_generation_stub(message: Message) -> None:
    """Illustrative handler; intentionally does not implement the interview flow."""
    # TODO: read validated answers from FSM, authenticate Telegram user,
    # debit credits transactionally, then call service.submit(...).
    _ = message, get_generation_service
