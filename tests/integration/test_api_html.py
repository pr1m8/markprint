"""Integration tests for HTML rendering."""

from __future__ import annotations

from markprint import RenderOptions, render_html


def test_render_html_from_raw_markdown() -> None:
    """Raw Markdown should become a styled HTML document."""
    styled = render_html(markdown="# Hello", options=RenderOptions(theme="default"))

    assert "<html" in styled.html
    assert "Hello" in styled.html
    assert "@page" in styled.css
