"""Snapshot testing helpers.

Purpose:
    Provide small utilities for binary and visual snapshot tests.

Design:
    Helpers intentionally avoid taking a dependency on a particular snapshot
    plugin so projects can use pytest-regressions, Syrupy, or custom golden
    files.

Examples:
    >>> snapshot_name("GitHub Theme")
    'github-theme'
"""

from __future__ import annotations

import re
from pathlib import Path


def snapshot_name(name: str) -> str:
    """Normalize text into a filesystem-friendly snapshot name.

    Args:
        name: Human-readable snapshot name.

    Returns:
        Normalized slug.

    Raises:
        None.

    Examples:
        >>> snapshot_name("Nord Theme")
        'nord-theme'
    """
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name.strip().lower())
    return slug.strip("-") or "snapshot"


def write_snapshot(path: Path, content: bytes) -> Path:
    """Write a binary snapshot.

    Args:
        path: Output path.
        content: Snapshot bytes.

    Returns:
        Output path.

    Raises:
        OSError: If the snapshot cannot be written.

    Examples:
        >>> write_snapshot(Path('x.bin'), b'data')  # doctest: +SKIP
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path
