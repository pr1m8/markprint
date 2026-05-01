"""Logging backend selection for Markprint.

Purpose:
    Provide a tiny logging facade so the core package can use structured log
    events without forcing an optional logging dependency.

Design:
    The standard-library backend is always available. The ``ultilog`` backend
    is imported lazily only when requested.

Examples:
    >>> from markprint.config.models import LoggingSettings
    >>> configure_logging(LoggingSettings(enabled=False))
"""

from __future__ import annotations

import logging

from markprint.config.models import LoggingSettings
from markprint.logging.stdlib import StdlibLoggingBackend


def configure_logging(settings: LoggingSettings) -> None:
    """Configure the selected logging backend.

    Args:
        settings: Logging settings.

    Returns:
        None.

    Raises:
        DependencyMissingError: If ``ultilog`` is requested but unavailable.

    Examples:
        >>> configure_logging(LoggingSettings(enabled=False))
    """
    if not settings.enabled:
        return
    if settings.backend == "ultilog":
        from markprint.logging.ultilog import UltilogBackend

        UltilogBackend().configure(settings)
        return
    StdlibLoggingBackend().configure(settings)


def get_logger(name: str) -> logging.Logger:
    """Return a logger for internal package use.

    Args:
        name: Logger name.

    Returns:
        Standard-library compatible logger.

    Raises:
        None.

    Examples:
        >>> get_logger("markprint").name
        'markprint'
    """
    return logging.getLogger(name)


__all__ = ["StdlibLoggingBackend", "configure_logging", "get_logger"]
