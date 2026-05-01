"""PDF inspection helpers."""

from __future__ import annotations

from pathlib import Path


def is_pdf(path: Path) -> bool:
    """Check whether a file starts with a PDF header.

    Args:
        path: File path.

    Returns:
        Whether the file appears to be a PDF.
    """
    return path.read_bytes().startswith(b"%PDF")
