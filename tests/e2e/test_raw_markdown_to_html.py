"""End-to-end raw Markdown HTML workflow."""

from __future__ import annotations

from markprint import RenderOptions, render_html


def test_raw_markdown_report_profile_html() -> None:
    """A report-profile raw document should render to full HTML."""
    markdown = """---\ntitle: Demo Report\nprofile: report\n---\n\n# Overview\n\nHello."""

    styled = render_html(markdown=markdown, options=RenderOptions(toc=True))

    assert "Demo Report" in styled.html
    assert "Overview" in styled.html
