"""Public Python API for Markprint.

Purpose:
    Expose ergonomic functions for rendering Markdown files, raw Markdown
    strings, and normalized sources to HTML or PDF.

Design:
    Public helpers normalize inputs into ``MarkdownSource`` and delegate all
    work to ``MarkdownToPdfPipeline``.

Examples:
    >>> html = render_html(markdown="# Hello")  # doctest: +SKIP
"""

from __future__ import annotations

from pathlib import Path

from markprint.config import list_profiles
from markprint.config.models import RenderOptions
from markprint.document.models import PdfArtifact, StyledHtmlDocument
from markprint.pipeline import MarkdownToPdfPipeline
from markprint.sources.models import MarkdownSource
from markprint.themes.registry import ThemeRegistry


def _source_from_args(
    source: str | Path | MarkdownSource | None = None,
    markdown: str | None = None,
    base_url: str | Path | None = None,
) -> MarkdownSource:
    """Normalize public API source arguments.

    Args:
        source: File path or normalized source.
        markdown: Raw Markdown string.
        base_url: Base path for raw Markdown assets.

    Returns:
        Normalized Markdown source.

    Raises:
        ValueError: If no source is provided or both source and markdown conflict.
    """
    if isinstance(source, MarkdownSource):
        if markdown is not None:
            raise ValueError("Provide either source or markdown, not both.")
        return source
    if markdown is not None:
        return MarkdownSource.from_text(markdown, base_dir=base_url)
    if source is None:
        raise ValueError("Provide either source or markdown.")
    return MarkdownSource.from_file(source)


def render_html(
    source: str | Path | MarkdownSource | None = None,
    *,
    markdown: str | None = None,
    options: RenderOptions | None = None,
    base_url: str | Path | None = None,
) -> StyledHtmlDocument:
    """Render Markdown to styled HTML.

    Args:
        source: File path or normalized source.
        markdown: Raw Markdown string.
        options: Render options.
        base_url: Base path for raw Markdown assets.

    Returns:
        Styled HTML document.

    Raises:
        ValueError: If no source is provided.
    """
    return MarkdownToPdfPipeline.default().render_html(
        _source_from_args(source, markdown, base_url),
        options,
    )


def render_pdf(
    source: str | Path | MarkdownSource | None = None,
    output: str | Path | None = None,
    *,
    markdown: str | None = None,
    options: RenderOptions | None = None,
    base_url: str | Path | None = None,
) -> PdfArtifact:
    """Render Markdown to PDF and optionally write it to disk.

    Args:
        source: File path or normalized source.
        output: Optional output path.
        markdown: Raw Markdown string.
        options: Render options.
        base_url: Base path for raw Markdown assets.

    Returns:
        PDF artifact.

    Raises:
        ValueError: If no source is provided.
    """
    opts = options or RenderOptions()
    if output is not None:
        opts = opts.model_copy(update={"output": Path(output)})
    return MarkdownToPdfPipeline.default().render(_source_from_args(source, markdown, base_url), opts)


def render_pdf_bytes(
    source: str | Path | MarkdownSource | None = None,
    *,
    markdown: str | None = None,
    options: RenderOptions | None = None,
    base_url: str | Path | None = None,
) -> bytes:
    """Render Markdown to PDF bytes.

    Args:
        source: File path or normalized source.
        markdown: Raw Markdown string.
        options: Render options.
        base_url: Base path for raw Markdown assets.

    Returns:
        PDF bytes.

    Raises:
        ValueError: If no source is provided.
    """
    return render_pdf(source, markdown=markdown, options=options, base_url=base_url).content


def list_themes() -> list[str]:
    """List built-in themes.

    Args:
        None.

    Returns:
        Theme names.

    Raises:
        None.

    Examples:
        >>> "default" in list_themes()
        True
    """
    return ThemeRegistry().list_builtin()


__all__ = [
    "list_profiles",
    "list_themes",
    "render_html",
    "render_pdf",
    "render_pdf_bytes",
]
