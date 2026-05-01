"""Document models used by the Markprint pipeline.

Purpose:
    Define intermediate representations passed between pipeline stages.

Examples:
    >>> Heading(level=1, title='Hello', slug='hello').slug
    'hello'
"""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class ParsedDocument(BaseModel):
    """Markdown body and metadata after frontmatter parsing."""

    model_config = ConfigDict(extra="forbid")

    body_markdown: str
    metadata: dict[str, object] = Field(default_factory=dict)
    source_path: Path | None = None
    base_dir: Path = Field(default_factory=Path.cwd)


class Heading(BaseModel):
    """Document heading."""

    level: int
    title: str
    slug: str


class HtmlDocument(BaseModel):
    """Rendered HTML body and extracted document structure."""

    body_html: str
    metadata: dict[str, object] = Field(default_factory=dict)
    headings: list[Heading] = Field(default_factory=list)
    base_url: Path = Field(default_factory=Path.cwd)


class StyledHtmlDocument(BaseModel):
    """Full printable HTML document."""

    html: str
    css: str
    base_url: Path = Field(default_factory=Path.cwd)


class PdfArtifact(BaseModel):
    """Rendered PDF artifact."""

    content: bytes
    output_path: Path | None = None
    page_count: int | None = None
    metadata: dict[str, str] = Field(default_factory=dict)
