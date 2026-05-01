"""Table-of-contents helpers."""

from __future__ import annotations

from markprint.document.models import Heading


def build_toc_html(headings: list[Heading]) -> str:
    """Build a simple nested-looking TOC as HTML.

    Args:
        headings: Document headings.

    Returns:
        HTML table of contents.

    Raises:
        None.

    Examples:
        >>> build_toc_html([Heading(level=1, title='A', slug='a')]).startswith('<nav')
        True
    """
    if not headings:
        return ""
    items = "\n".join(
        f'<li class="toc-level-{heading.level}"><a href="#{heading.slug}">{heading.title}</a></li>'
        for heading in headings
    )
    return f'<nav class="toc"><h2>Contents</h2><ol>{items}</ol></nav>'
