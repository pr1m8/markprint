"""Standard-library logging backend for Markprint.

Purpose:
    Configure Python's built-in logging module when no optional logging
    backend is selected.
"""

from __future__ import annotations

import logging

from markprint.config.models import LoggingSettings


class StdlibLoggingBackend:
    """Configure standard-library logging.

    Args:
        None.

    Returns:
        A backend instance.

    Raises:
        None.

    Examples:
        >>> StdlibLoggingBackend().__class__.__name__
        'StdlibLoggingBackend'
    """

    def configure(self, settings: LoggingSettings) -> None:
        """Configure stdlib logging.

        Args:
            settings: Logging settings.

        Returns:
            None.

        Raises:
            None.

        Examples:
            >>> StdlibLoggingBackend().configure(LoggingSettings(enabled=False))
        """
        if not settings.enabled:
            return
        level = getattr(logging, settings.level.upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            force=settings.force,
            format="%(levelname)s %(name)s: %(message)s",
        )

    def get_logger(self, name: str) -> logging.Logger:
        """Return a standard logger.

        Args:
            name: Logger name.

        Returns:
            Logger instance.

        Raises:
            None.
        """
        return logging.getLogger(name)
