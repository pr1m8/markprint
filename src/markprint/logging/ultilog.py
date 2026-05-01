"""Optional ultilog logging backend."""
from __future__ import annotations
from typing import Any
from markprint.config.models import LoggingSettings
from markprint.diagnostics.errors import DependencyMissingError
class UltilogBackend:
    """Configure logging through ultilog when installed."""
    def configure(self, settings: LoggingSettings) -> None:
        """Configure ultilog.

        Args:
            settings: Logging settings.

        Returns:
            None.

        Raises:
            DependencyMissingError: If ultilog is unavailable.
        """
        if not settings.enabled:
            return
        try:
            from ultilog import setup_dev, setup_prod, setup_test
        except ImportError as exc:  # pragma: no cover
            raise DependencyMissingError("ultilog is not installed. Install with: pip install 'markprint[logging]'") from exc
        kwargs: dict[str, Any] = {"level": settings.level, "force": settings.force}
        if settings.preset == "dev":
            setup_dev(**kwargs)
        elif settings.preset == "test":
            setup_test(**kwargs)
        else:
            setup_prod(**kwargs)
    def get_logger(self, name: str):
        """Return an ultilog logger.

        Args:
            name: Logger name.

        Returns:
            Ultilog logger.

        Raises:
            DependencyMissingError: If ultilog is unavailable.
        """
        try:
            from ultilog import get_logger
        except ImportError as exc:  # pragma: no cover
            raise DependencyMissingError("ultilog is not installed. Install with: pip install 'markprint[logging]'") from exc
        return get_logger(name)
