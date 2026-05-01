"""Configuration merge helpers.

Purpose:
    Merge dictionaries from defaults, config files, frontmatter, API options,
    and CLI flags into a final ``RenderOptions`` model.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def deep_merge(*configs: Mapping[str, Any]) -> dict[str, Any]:
    """Deep merge configuration dictionaries.

    Args:
        *configs: Configuration mappings in increasing precedence order.

    Returns:
        A merged dictionary.

    Raises:
        None.

    Examples:
        >>> deep_merge({"a": {"x": 1}}, {"a": {"y": 2}})
        {'a': {'x': 1, 'y': 2}}
    """
    merged: dict[str, Any] = {}
    for config in configs:
        for key, value in config.items():
            if isinstance(value, Mapping) and isinstance(merged.get(key), dict):
                merged[key] = deep_merge(merged[key], value)
            else:
                merged[key] = value
    return merged
