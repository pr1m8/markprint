"""Optional Python-Markdown engine."""
from __future__ import annotations
from markprint.config.models import RenderOptions
from markprint.document.headings import extract_headings
from markprint.document.models import HtmlDocument, ParsedDocument
from markprint.diagnostics.errors import DependencyMissingError
class PythonMarkdownEngine:
    """Render Markdown with Python-Markdown and pymdown extensions."""
    name = "python-markdown"
    def render(self, document: ParsedDocument, options: RenderOptions) -> HtmlDocument:
        """Render Markdown using the optional Python-Markdown backend.

        Args:
            document: Parsed Markdown document.
            options: Render options.

        Returns:
            Rendered HTML document.

        Raises:
            DependencyMissingError: If optional dependencies are absent.
        """
        try:
            import markdown
        except ImportError as exc:  # pragma: no cover
            raise DependencyMissingError("Install with: pip install 'markprint[markdown-python]'" ) from exc
        extensions = ["extra", "toc", "tables", "fenced_code", "codehilite"]
        html = markdown.markdown(document.body_markdown, extensions=extensions, output_format="html5")
        return HtmlDocument(body_html=html, metadata=document.metadata, headings=extract_headings(document.body_markdown), base_url=document.base_dir)
