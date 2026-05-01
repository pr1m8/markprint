"""Source loading helpers for Markprint.

Purpose:
    Convert CLI/API input values into normalized ``MarkdownSource`` models.
"""

from __future__ import annotations

from pathlib import Path

from markprint.sources.models import MarkdownSource


def load_source(path: str | Path) -> MarkdownSource:
    """Load a Markdown source from a path or stdin marker.

    Args:
        path: File path or ``-`` for stdin. Stdin is handled by the CLI because
            this function does not read from process streams.

    Returns:
        A loaded Markdown source.

    Raises:
        ValueError: If ``path`` is ``-``.
        FileNotFoundError: If a file path does not exist.

    Examples:
        >>> load_source("README.md")  # doctest: +SKIP
    """
    if str(path) == "-":
        raise ValueError("stdin marker '-' must be handled by the CLI stream reader.")
    return MarkdownSource.from_file(path)
