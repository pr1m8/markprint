"""WeasyPrint renderer backend."""
from __future__ import annotations
from markprint.config.models import RenderOptions
from markprint.document.models import PdfArtifact, StyledHtmlDocument
from markprint.diagnostics.errors import DependencyMissingError, RenderError
class WeasyPrintRenderer:
    """Render styled HTML with WeasyPrint."""
    name = "weasyprint"
    def render(self, document: StyledHtmlDocument, options: RenderOptions) -> PdfArtifact:
        """Render styled HTML to PDF bytes.

        Args:
            document: Styled HTML document.
            options: Render options.

        Returns:
            PDF artifact.

        Raises:
            DependencyMissingError: If WeasyPrint is unavailable.
            RenderError: If rendering fails.
        """
        try:
            from weasyprint import HTML
        except ImportError as exc:  # pragma: no cover
            raise DependencyMissingError("Install WeasyPrint: pip install weasyprint") from exc
        try:
            content = HTML(string=document.html, base_url=str(document.base_url)).write_pdf()
        except Exception as exc:  # pragma: no cover
            raise RenderError(f"WeasyPrint render failed: {exc}") from exc
        return PdfArtifact(content=bytes(content))
