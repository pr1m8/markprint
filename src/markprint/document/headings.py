"""Heading extraction helpers."""

from __future__ import annotations

import re

from markprint.document.models import Heading

_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


def slugify(text: str) -> str:
    """Create a URL-friendly heading slug.

    Args:
        text: Heading text.

    Returns:
        Slugified text.

    Raises:
        None.

    Examples:
        >>> slugify('Hello World!')
        'hello-world'
    """
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    return re.sub(r"[\s-]+", "-", slug)


def extract_headings(markdown: str) -> list[Heading]:
    """Extract Markdown ATX headings.

    Args:
        markdown: Markdown text.

    Returns:
        Heading models.

    Raises:
        None.

    Examples:
        >>> extract_headings('# A\n## B')[1].level
        2
    """
    return [
        Heading(level=len(m.group(1)), title=m.group(2), slug=slugify(m.group(2)))
        for m in _HEADING_RE.finditer(markdown)
    ]
