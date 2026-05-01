"""PDF renderer protocol."""

from __future__ import annotations

from typing import Protocol

from markprint.config.models import RenderOptions
from markprint.document.models import PdfArtifact, StyledHtmlDocument


class PdfRenderer(Protocol):
    """Convert styled HTML to a PDF artifact."""

    name: str

    def render(self, document: StyledHtmlDocument, options: RenderOptions) -> PdfArtifact:
        """Render styled HTML to PDF.

        Args:
            document: Styled HTML document.
            options: Render options.

        Returns:
            PDF artifact.

        Raises:
            Exception: Backend-specific render errors.
        """
        ...
