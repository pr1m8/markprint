"""Optional Playwright PDF renderer."""
from __future__ import annotations
import tempfile
from pathlib import Path
from markprint.config.models import RenderOptions
from markprint.document.models import PdfArtifact, StyledHtmlDocument
from markprint.diagnostics.errors import DependencyMissingError
class PlaywrightRenderer:
    """Render styled HTML through Chromium with Playwright."""
    name = "playwright"
    def render(self, document: StyledHtmlDocument, options: RenderOptions) -> PdfArtifact:
        """Render styled HTML to PDF using Playwright.

        Args:
            document: Styled HTML document.
            options: Render options.

        Returns:
            PDF artifact.

        Raises:
            DependencyMissingError: If Playwright is unavailable.
        """
        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:  # pragma: no cover
            raise DependencyMissingError("Install with: pip install 'markprint[browser]' and run playwright install chromium") from exc
        with tempfile.TemporaryDirectory() as tmp:
            html_path = Path(tmp) / "document.html"
            html_path.write_text(document.html, encoding="utf-8")
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(html_path.as_uri(), wait_until="networkidle")
                pdf = page.pdf(format=options.page_size, print_background=True)
                browser.close()
        return PdfArtifact(content=pdf)
