"""Optional Pandoc renderer."""
from __future__ import annotations
import tempfile
from pathlib import Path
from markprint.config.models import RenderOptions
from markprint.document.models import PdfArtifact, StyledHtmlDocument
from markprint.diagnostics.errors import DependencyMissingError
class PandocRenderer:
    """Render styled HTML to PDF with Pandoc where available."""
    name = "pandoc"
    def render(self, document: StyledHtmlDocument, options: RenderOptions) -> PdfArtifact:
        """Render HTML to PDF using pypandoc.

        Args:
            document: Styled HTML document.
            options: Render options.

        Returns:
            PDF artifact.

        Raises:
            DependencyMissingError: If pypandoc is unavailable.
        """
        try:
            import pypandoc
        except ImportError as exc:  # pragma: no cover
            raise DependencyMissingError("Install with: pip install 'markprint[pandoc]' or 'markprint[pandoc-binary]'" ) from exc
        with tempfile.TemporaryDirectory() as tmp:
            html = Path(tmp) / "document.html"
            pdf = Path(tmp) / "document.pdf"
            html.write_text(document.html, encoding="utf-8")
            pypandoc.convert_file(str(html), "pdf", outputfile=str(pdf))
            return PdfArtifact(content=pdf.read_bytes())
