"""Markdown engine protocols."""

from __future__ import annotations

from typing import Protocol

from markprint.config.models import RenderOptions
from markprint.document.models import HtmlDocument, ParsedDocument


class MarkdownEngine(Protocol):
    """Convert parsed Markdown into an HTML document."""

    name: str

    def render(self, document: ParsedDocument, options: RenderOptions) -> HtmlDocument:
        """Render parsed Markdown to HTML.

        Args:
            document: Parsed Markdown document.
            options: Render options.

        Returns:
            Rendered HTML document.

        Raises:
            Exception: Backend-specific errors.
        """
        ...
