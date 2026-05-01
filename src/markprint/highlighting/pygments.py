"""Pygments syntax highlighting helpers."""

from __future__ import annotations


def get_pygments_css(style: str = "default", cssclass: str = "highlight") -> str:
    """Return Pygments CSS for a style.

    Args:
        style: Pygments style name.
        cssclass: CSS class used around highlighted blocks.

    Returns:
        CSS string.

    Raises:
        ImportError: If Pygments is unavailable.

    Examples:
        >>> '.highlight' in get_pygments_css()
        True
    """
    from pygments.formatters import HtmlFormatter

    return HtmlFormatter(style=style, cssclass=cssclass).get_style_defs(f".{cssclass}")
