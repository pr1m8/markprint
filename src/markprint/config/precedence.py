"""Configuration precedence helpers.

Purpose:
    Convert loose configuration dictionaries into validated render options.
"""

from __future__ import annotations

from typing import Any

from markprint.config.merge import deep_merge
from markprint.config.models import RenderOptions


def build_options(*configs: dict[str, Any]) -> RenderOptions:
    """Build render options from configuration dictionaries.

    Args:
        *configs: Configuration dictionaries in increasing precedence order.

    Returns:
        Validated render options.

    Raises:
        pydantic.ValidationError: If merged values are invalid.

    Examples:
        >>> build_options({"theme": "github"}).theme
        'github'
    """
    return RenderOptions.model_validate(deep_merge(*configs))
