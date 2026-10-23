"""Tests for the Gemini service without network access."""

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app.config.settings import Settings
from app.services.gemini_service import GeminiService, GeminiServiceError


@pytest.fixture
def settings() -> Settings:
    return Settings(
        gemini_api_key="test-key",
        gemini_model="gemini-test-model",
        temperature=0.4,
    )


def test_service_initializes_official_client(monkeypatch, settings: Settings) -> None:
    client = Mock()
    client_constructor = Mock(return_value=client)
    monkeypatch.setattr("app.services.gemini_service.genai.Client", client_constructor)

    service = GeminiService(settings)

    client_constructor.assert_called_once_with(api_key="test-key")
    assert service._client is client


def test_generate_answer_sends_conversation_and_returns_text(settings: Settings) -> None:
    client = Mock()
    client.models.generate_content.return_value = SimpleNamespace(text="A helpful answer.")
    service = GeminiService(settings, client=client)
    messages = [
        {"role": "user", "content": "What is 2 + 2?"},
        {"role": "assistant", "content": "4."},
        {"role": "user", "content": "Why?"},
    ]

    answer = service.generate_answer(messages)

    assert answer == "A helpful answer."
    client.models.generate_content.assert_called_once()
    request = client.models.generate_content.call_args.kwargs
    assert request["model"] == "gemini-test-model"
    assert request["config"].temperature == 0.4
    assert request["config"].system_instruction
    assert [turn.role for turn in request["contents"]] == ["user", "model", "user"]
    assert [turn.parts[0].text for turn in request["contents"]] == [
        "What is 2 + 2?",
        "4.",
        "Why?",
    ]


def test_generate_answer_wraps_api_errors_safely(
    monkeypatch, settings: Settings
) -> None:
    class FakeAPIError(Exception):
        pass

    monkeypatch.setattr("app.services.gemini_service.errors.APIError", FakeAPIError)
    client = Mock()
    client.models.generate_content.side_effect = FakeAPIError("sensitive internal detail")
    service = GeminiService(settings, client=client)

    with pytest.raises(GeminiServiceError) as error:
        service.generate_answer([{"role": "user", "content": "Hello"}])

    assert "sensitive internal detail" not in str(error.value)