"""Load and validate application settings."""

import os
from dataclasses import dataclass, field
from typing import Mapping

from dotenv import load_dotenv

DEFAULT_MODEL = "gemini-3.8-flash"
DEFAULT_TEMPERATURE = 0.2


class ConfigurationError(ValueError):
    """Raised when required application configuration is invalid."""


@dataclass(frozen=True)
class Settings:
    """Validated settings used by the application and Gemini service."""

    gemini_api_key: str = field(repr=False)
    gemini_model: str = DEFAULT_MODEL
    temperature: float = DEFAULT_TEMPERATURE


def load_settings(environ: Mapping[str, str] | None = None) -> Settings:
    """Load settings from the environment, loading `.env` when appropriate."""
    if environ is None:
        load_dotenv()
        environ = os.environ

    api_key = environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise ConfigurationError(
            "GEMINI_API_KEY is missing. Add your Gemini API key to the .env file."
        )

    model = environ.get("GEMINI_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL
    raw_temperature = environ.get("TEMPERATURE", str(DEFAULT_TEMPERATURE)).strip()
    try:
        temperature = float(raw_temperature)
    except ValueError as error:
        raise ConfigurationError("TEMPERATURE must be a number between 0 and 2.") from error

    if not 0 <= temperature <= 2:
        raise ConfigurationError("TEMPERATURE must be a number between 0 and 2.")

    return Settings(
        gemini_api_key=api_key,
        gemini_model=model,
        temperature=temperature,
    )