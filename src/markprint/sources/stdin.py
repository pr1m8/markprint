"""Stdin helpers for Markprint."""

from __future__ import annotations

import sys

from markprint.sources.models import MarkdownSource


def read_stdin() -> MarkdownSource:
    """Read Markdown from standard input.

    Args:
        None.

    Returns:
        A stdin-backed Markdown source.

    Raises:
        UnicodeDecodeError: If stdin cannot be decoded.

    Examples:
        >>> read_stdin()  # doctest: +SKIP
    """
    return MarkdownSource.from_stdin(sys.stdin.read())
