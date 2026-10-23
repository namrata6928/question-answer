"""Tests for application configuration."""

import pytest

from app.config.settings import (
    DEFAULT_MODEL,
    ConfigurationError,
    load_settings,
)


def test_load_settings_uses_defaults_and_environment_values() -> None:
    settings = load_settings(
        {
            "GEMINI_API_KEY": "test-key",
            "GEMINI_MODEL": "gemini-test-model",
            "TEMPERATURE": "0.7",
        }
    )

    assert settings.gemini_api_key == "test-key"
    assert settings.gemini_model == "gemini-test-model"
    assert settings.temperature == 0.7


def test_load_settings_uses_sensible_defaults() -> None:
    settings = load_settings({"GEMINI_API_KEY": "test-key"})

    assert settings.gemini_model == DEFAULT_MODEL
    assert settings.temperature == 0.2


def test_load_settings_requires_api_key() -> None:
    with pytest.raises(ConfigurationError, match="GEMINI_API_KEY"):
        load_settings({})


def test_load_settings_rejects_invalid_temperature() -> None:
    with pytest.raises(ConfigurationError, match="TEMPERATURE"):
        load_settings({"GEMINI_API_KEY": "test-key", "TEMPERATURE": "3"})