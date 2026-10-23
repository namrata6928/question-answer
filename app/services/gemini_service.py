"""Google Gemini API integration using the official Gen AI SDK."""

import logging
from collections.abc import Mapping, Sequence

from google import genai
from google.genai import errors, types

from app.config.settings import Settings
from app.prompts.qa_prompt import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

ChatMessage = Mapping[str, str]


class GeminiServiceError(RuntimeError):
    """A safe, user-facing error from the Gemini service."""


class GeminiService:
    """Generate answers while keeping API communication outside the UI."""

    def __init__(self, settings: Settings, client: genai.Client | None = None) -> None:
        self._settings = settings
        self._client = client if client is not None else genai.Client(
            api_key=settings.gemini_api_key
        )

    def generate_answer(self, messages: Sequence[ChatMessage]) -> str:
        """Return an answer for the supplied user/assistant conversation turns."""
        contents = [
            types.Content(
                role="model" if message["role"] == "assistant" else "user",
                parts=[types.Part.from_text(text=message["content"])],
            )
            for message in messages
        ]

        try:
            response = self._client.models.generate_content(
                model=self._settings.gemini_model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=self._settings.temperature,
                ),
            )
        except errors.APIError as error:
            logger.error("Gemini request failed (%s)", type(error).__name__)
            raise GeminiServiceError(
                "The AI service could not complete your request. Please try again."
            ) from None

        answer = response.text
        if not answer or not answer.strip():
            raise GeminiServiceError(
                "The AI returned an empty response. Please try asking again."
            )
        return answer