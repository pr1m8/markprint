"""Unit tests for frontmatter parsing."""
import pytest
from markprint.frontmatter import FrontmatterParser
from markprint.sources.models import MarkdownSource

def test_parse_frontmatter() -> None:
    pytest.importorskip("frontmatter")
    doc = FrontmatterParser().parse(MarkdownSource.from_text("---\ntitle: Hi\n---\n# Body"))
    assert doc.metadata["title"] == "Hi"
    assert "# Body" in doc.body_markdown
