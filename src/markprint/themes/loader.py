"""Convenience theme loader."""

from __future__ import annotations

from markprint.themes.models import ThemeSpec
from markprint.themes.registry import ThemeRegistry


def load_theme(name_or_path: str) -> ThemeSpec:
    """Load a theme.

    Args:
        name_or_path: Built-in theme name or path.

    Returns:
        Loaded theme spec.

    Raises:
        ThemeError: If the theme is unknown.
    """
    return ThemeRegistry().load(name_or_path)
