"""Configuration discovery for Markprint.

Purpose:
    Load Markprint configuration from ``markprint.toml``, ``.markprint.toml``,
    or ``pyproject.toml``.

Design:
    Discovery returns dictionaries so precedence merging can be tested
    separately from filesystem lookup.

Examples:
    >>> discover_config(start_dir=None)
    {}
"""

from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Any


def discover_config(start_dir: str | Path | None = None) -> dict[str, Any]:
    """Discover and load project configuration.

    Args:
        start_dir: Directory where discovery should begin.

    Returns:
        A dictionary of configuration values.

    Raises:
        OSError: If a discovered file cannot be read.
        tomllib.TOMLDecodeError: If a discovered TOML file is invalid.

    Examples:
        >>> isinstance(discover_config(None), dict)
        True
    """
    if start_dir is None:
        return {}
    root = Path(start_dir).resolve()
    candidates = [root / "markprint.toml", root / ".markprint.toml", root / "pyproject.toml"]
    for candidate in candidates:
        if not candidate.exists():
            continue
        data = tomllib.loads(candidate.read_text(encoding="utf-8"))
        if candidate.name == "pyproject.toml":
            return data.get("tool", {}).get("markprint", {})
        return data
    return {}
