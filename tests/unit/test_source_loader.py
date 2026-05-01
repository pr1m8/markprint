"""Unit tests for source loading."""

from markprint.sources.models import MarkdownSource


def test_from_text() -> None:
    source = MarkdownSource.from_text("# Hi")
    assert source.kind == "string"
    assert source.text == "# Hi"


def test_from_stdin() -> None:
    source = MarkdownSource.from_stdin("# Hi")
    assert source.kind == "stdin"
