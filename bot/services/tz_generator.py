"""Technical specification generation service boundary."""

from bot.services.llm import LLMService


class TZGenerator:
    """Coordinates future transformation of collected answers into a ТЗ."""

    def __init__(self, llm_service: LLMService) -> None:
        self._llm_service = llm_service

    async def generate_tz(self, answers: dict[str, str]) -> str:
        """Generate a technical specification from collected answers."""
        # TODO: define the input contract and delegate generation to the LLM service.
        raise NotImplementedError("Technical specification generation is not implemented yet")
