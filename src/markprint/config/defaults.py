"""Default configuration values for Markprint.

Purpose:
    Centralize built-in defaults used when no project configuration exists.
"""

from markprint.config.models import RenderOptions

DEFAULT_OPTIONS = RenderOptions()

__all__ = ["DEFAULT_OPTIONS"]
