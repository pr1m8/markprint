"""Configuration utilities for Markprint.

Purpose:
    Expose validated models, config discovery helpers, merge utilities, and
    document profile defaults.
"""

from markprint.config.discovery import discover_config
from markprint.config.merge import deep_merge
from markprint.config.models import LoggingSettings, PathSettings, RenderOptions
from markprint.config.profiles import get_profile_defaults, list_profiles

__all__ = [
    "LoggingSettings",
    "PathSettings",
    "RenderOptions",
    "deep_merge",
    "discover_config",
    "get_profile_defaults",
    "list_profiles",
]
