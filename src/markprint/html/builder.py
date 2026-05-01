"""HTML document builder for Markprint.

Purpose:
    Build a full printable HTML document from rendered Markdown body HTML.

Design:
    This implementation intentionally avoids mandatory template-engine imports
    so the core pipeline remains lightweight and easy to test. Theme CSS is
    loaded from bundled package resources.
"""

from __future__ import annotations

from importlib.resources import files

from markprint.config.models import RenderOptions
from markprint.document.models import HtmlDocument, StyledHtmlDocument


class HtmlBuilder:
    """Build a full styled HTML document.

    Args:
        None.

    Returns:
        Builder instance.

    Raises:
        None.

    Examples:
        >>> HtmlBuilder().__class__.__name__
        'HtmlBuilder'
    """

    def build(self, document: HtmlDocument, options: RenderOptions) -> StyledHtmlDocument:
        """Build full HTML and CSS.

        Args:
            document: Rendered HTML body and metadata.
            options: Render options.

        Returns:
            Styled HTML document.

        Raises:
            None.
        """
        css = self._load_theme_css(options.theme)
        title = str(document.metadata.get("title") or "Markprint Document")
        toc = self._render_toc(document, options)
        html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <style>{css}</style>
</head>
<body class="markprint theme-{options.theme}">
  <main class="document">
    {toc}
    {document.body_html}
  </main>
</body>
</html>
"""
        return StyledHtmlDocument(html=html, css=css, base_url=document.base_url)

    def _render_toc(self, document: HtmlDocument, options: RenderOptions) -> str:
        """Render an optional table of contents.

        Args:
            document: HTML document with heading metadata.
            options: Render options.

        Returns:
            HTML TOC or an empty string.

        Raises:
            None.
        """
        if not options.toc or not document.headings:
            return ""
        items = "\n".join(
            f'<li class="toc-level-{heading.level}">'
            f'<a href="#{heading.slug}">{heading.title}</a></li>'
            for heading in document.headings
        )
        return f'<nav class="toc"><h2>Contents</h2><ul>{items}</ul></nav>'

    def _load_theme_css(self, theme: str) -> str:
        """Load bundled theme CSS.

        Args:
            theme: Theme name.

        Returns:
            CSS text.

        Raises:
            FileNotFoundError: If the default theme is missing.
        """
        root = files("markprint.themes.builtin")
        candidate = root / theme / "theme.css"
        if not candidate.is_file():
            candidate = root / "default" / "theme.css"
        return candidate.read_text(encoding="utf-8")
