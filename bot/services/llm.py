"""Abstraction boundary for OpenAI-compatible LLM providers."""

from abc import ABC, abstractmethod


class LLMService(ABC):
    """Interface for asynchronous text generation providers."""

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate text from input text; provider behavior is implementation-specific."""
        raise NotImplementedError


class OpenAICompatibleLLMService(LLMService):
    """Placeholder for an OpenAI-compatible API client implementation."""

    def __init__(self, *, api_key: str, base_url: str, model: str) -> None:
        self._api_key = api_key
        self._base_url = base_url
        self._model = model

    async def generate(self, prompt: str) -> str:
        """Return generated text once provider communication is implemented."""
        # TODO: call the configured OpenAI-compatible API asynchronously.
        raise NotImplementedError("LLM API integration is not implemented yet")
