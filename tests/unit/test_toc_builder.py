"""Unit tests for TOC building."""

from markprint.document.headings import extract_headings
from markprint.document.toc import build_toc_html


def test_toc_html() -> None:
    headings = extract_headings("# A\n## B")
    html = build_toc_html(headings)
    assert "Contents" in html
    assert "toc-level-2" in html
