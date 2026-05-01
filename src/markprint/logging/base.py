"""Logging backend protocol."""

from __future__ import annotations

import logging
from typing import Protocol

from markprint.config.models import LoggingSettings


class LoggingBackend(Protocol):
    """Configure and provide loggers."""

    def configure(self, settings: LoggingSettings) -> None:
        """Configure logging.

        Args:
            settings: Logging settings.

        Returns:
            None.
        """
        ...

    def get_logger(self, name: str) -> logging.Logger:
        """Return a logger.

        Args:
            name: Logger name.

        Returns:
            Logger-like object.
        """
        ...
