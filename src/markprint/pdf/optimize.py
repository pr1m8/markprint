"""PDF optimization placeholders."""

from __future__ import annotations

from pathlib import Path


def optimize_pdf(path: Path) -> Path:
    """Return a path unchanged until optimization backends are enabled.

    Args:
        path: PDF path.

    Returns:
        The same path.
    """
    return path
