"""Glob expansion helpers for batch rendering."""

from __future__ import annotations

from glob import glob
from pathlib import Path


def expand_inputs(patterns: list[str]) -> list[Path]:
    """Expand glob patterns to Markdown input paths.

    Args:
        patterns: Input paths or glob patterns.

    Returns:
        Sorted, unique paths.

    Raises:
        None.

    Examples:
        >>> expand_inputs([])
        []
    """
    paths: set[Path] = set()
    for pattern in patterns:
        matches = glob(pattern)
        if matches:
            paths.update(Path(match) for match in matches)
        else:
            paths.add(Path(pattern))
    return sorted(paths)
