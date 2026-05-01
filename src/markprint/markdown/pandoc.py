"""Pandoc Markdown placeholder engine."""

from __future__ import annotations

from markprint.config.models import RenderOptions
from markprint.diagnostics.errors import DependencyMissingError
from markprint.document.models import HtmlDocument, ParsedDocument


class PandocMarkdownEngine:
    """Render Markdown to HTML using Pandoc through pypandoc."""

    name = "pandoc"

    def render(self, document: ParsedDocument, options: RenderOptions) -> HtmlDocument:
        """Render Markdown using Pandoc.

        Args:
            document: Parsed Markdown document.
            options: Render options.

        Returns:
            Rendered HTML document.

        Raises:
            DependencyMissingError: If pypandoc is absent.
        """
        try:
            import pypandoc
        except ImportError as exc:  # pragma: no cover
            raise DependencyMissingError("Install with: pip install 'markprint[pandoc]'") from exc
        html = pypandoc.convert_text(document.body_markdown, "html", format="md")
        return HtmlDocument(
            body_html=str(html), metadata=document.metadata, base_url=document.base_dir
        )
