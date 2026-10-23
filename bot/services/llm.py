from abc import ABC, abstractmethod
from openai import AsyncOpenAI


class LLMService(ABC):
    @abstractmethod
    async def generate(self, messages: list[dict], temperature: float = 0.7) -> str:
        pass

class OpenAICompatibleLLMService(LLMService):
    def __init__(self, *, api_key: str, base_url: str, model: str) -> None:
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self._model = model
    async def generate(self, messages: list[dict], temperature: float = 0.7) -> str:
        responce = await self._client.chat.completions.create(
            model=self._model,
            messages=messages,
            temperature=temperature,
            tool_choice="none",
        )
        return responce.choices[0].message.content.strip()

