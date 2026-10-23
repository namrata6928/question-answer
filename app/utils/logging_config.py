"""Application logging setup."""

import logging


def configure_logging() -> None:
    """Configure concise application logs without recording user content."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )