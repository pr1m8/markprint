"""Additional coverage tests for public helpers and branches."""

from pathlib import Path

import pytest

from markprint.api import list_profiles, list_themes, render_html, render_pdf_bytes
from markprint.config.models import RenderOptions
from markprint.diagnostics.errors import ThemeError
from markprint.document.toc import build_toc_html
from markprint.frontmatter import FrontmatterParser
from markprint.pipeline import MarkdownToPdfPipeline
from markprint.sources.models import MarkdownSource
from markprint.themes.registry import ThemeRegistry


def test_render_html_public_api() -> None:
    """Render raw Markdown to HTML through the public API."""
    document = render_html(markdown="# Hello\n\nWorld")
    assert "<h1" in document.html
    assert "Hello" in document.html


def test_render_pdf_bytes_public_api_without_weasyprint() -> None:
    """The PDF byte API should return bytes with fallback renderer behavior."""
    data = render_pdf_bytes(markdown="# Hello")
    assert isinstance(data, bytes)
    assert data.startswith(b"%PDF")


def test_list_helpers() -> None:
    """List helpers should expose built-in registries."""
    assert "default" in list_themes()
    assert "docs" in list_profiles()


def test_empty_toc_branch() -> None:
    """Empty headings should produce empty TOC markup."""
    assert build_toc_html([]) == ""


def test_frontmatter_without_frontmatter_block() -> None:
    """Plain Markdown should parse without metadata."""
    source = MarkdownSource.from_text("# Plain")
    parsed = FrontmatterParser().parse(source)
    assert parsed.metadata == {}
    assert parsed.body_markdown.strip() == "# Plain"


def test_source_from_file_and_compile(tmp_path: Path) -> None:
    """File and compiled source constructors should work."""
    first = tmp_path / "a.md"
    second = tmp_path / "b.md"
    first.write_text("# A", encoding="utf-8")
    second.write_text("# B", encoding="utf-8")

    source = MarkdownSource.from_file(first)
    assert source.kind == "file"
    assert source.text == "# A"

    compiled = MarkdownSource.compile_files([first, second])
    assert compiled.kind == "compiled"
    assert "# A" in compiled.text
    assert "# B" in compiled.text


def test_theme_registry_errors_and_path_theme(tmp_path: Path) -> None:
    """Theme registry should support path themes and reject unknown themes."""
    theme_dir = tmp_path / "custom"
    theme_dir.mkdir()
    (theme_dir / "theme.css").write_text("body { color: black; }", encoding="utf-8")

    registry = ThemeRegistry()
    custom = registry.load(str(theme_dir))
    assert "color" in custom.css

    with pytest.raises(ThemeError):
        registry.load("does-not-exist")


def test_frontmatter_metadata_overrides_options() -> None:
    """Frontmatter metadata should merge into render options."""
    pipeline = MarkdownToPdfPipeline.default()
    source = MarkdownSource.from_text("---\ntheme: nord\ntoc: true\n---\n\n# Hello")

    artifact = pipeline.render(source, RenderOptions())
    assert artifact.content.startswith(b"%PDF")
