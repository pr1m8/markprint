"""Document profiles for Markprint.

Purpose:
    Provide named bundles of rendering defaults such as report, resume,
    docs, academic, and book-style output.

Design:
    Profiles are plain dictionaries intentionally kept separate from
    ``RenderOptions`` so they can be merged with configuration files,
    frontmatter, CLI flags, and future plugin-provided profiles.

Attributes:
    BUILTIN_PROFILES: Built-in profile defaults keyed by profile name.

Examples:
    >>> get_profile_defaults("report")["toc"]
    True
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

BUILTIN_PROFILES: dict[str, dict[str, Any]] = {
    "docs": {
        "theme": "github",
        "toc": False,
        "page_numbers": True,
        "code_theme": "default",
    },
    "report": {
        "theme": "report",
        "toc": True,
        "page_numbers": True,
        "code_theme": "github-dark",
        "margin": "0.75in",
    },
    "resume": {
        "theme": "resume",
        "toc": False,
        "page_numbers": False,
        "code_theme": "default",
        "margin": "0.45in",
    },
    "academic": {
        "theme": "academic",
        "toc": True,
        "page_numbers": True,
        "code_theme": "default",
        "margin": "1in",
    },
    "book": {
        "theme": "academic",
        "toc": True,
        "page_numbers": True,
        "code_theme": "default",
        "margin": "0.9in",
    },
    "whitepaper": {
        "theme": "report",
        "toc": True,
        "page_numbers": True,
        "code_theme": "github-dark",
        "margin": "0.8in",
    },
}


def list_profiles() -> list[str]:
    """Return available built-in profile names.

    Args:
        None.

    Returns:
        Sorted built-in profile names.

    Raises:
        None.

    Examples:
        >>> "report" in list_profiles()
        True
    """
    return sorted(BUILTIN_PROFILES)


def get_profile_defaults(name: str) -> dict[str, Any]:
    """Return a copy of built-in defaults for a profile.

    Args:
        name: Profile name.

    Returns:
        Profile defaults.

    Raises:
        KeyError: If the profile is unknown.

    Examples:
        >>> get_profile_defaults("docs")["theme"]
        'github'
    """
    return deepcopy(BUILTIN_PROFILES[name])
