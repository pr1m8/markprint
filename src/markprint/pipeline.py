"""Markdown-to-PDF rendering pipeline.

Purpose:
    Coordinate source loading, frontmatter parsing, Markdown rendering,
    HTML building, PDF rendering, debug artifact emission, and output writing.

Design:
    The pipeline selects engines from user options while preserving strict
    stage boundaries. Frontmatter metadata can adjust render options, but
    explicit ``RenderOptions`` values supplied by the caller retain priority
    for the fields already set by the caller.

Examples:
    >>> from markprint.sources.models import MarkdownSource
    >>> pipeline = MarkdownToPdfPipeline.default()
    >>> artifact = pipeline.render(MarkdownSource.from_text('# Hi'))  # doctest: +SKIP
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from markprint.config.models import RenderOptions
from markprint.config.profiles import get_profile_defaults
from markprint.document.models import PdfArtifact, StyledHtmlDocument
from markprint.frontmatter import FrontmatterParser
from markprint.html import HtmlBuilder
from markprint.logging import configure_logging, get_logger
from markprint.markdown import MarkdownItEngine, PandocMarkdownEngine, PythonMarkdownEngine
from markprint.renderers import PandocRenderer, PlaywrightRenderer, WeasyPrintRenderer
from markprint.sources.models import MarkdownSource


class MarkdownToPdfPipeline:
    """Coordinate a Markdown-to-PDF render operation.

    Args:
        None.

    Returns:
        A rendering pipeline instance.

    Raises:
        None.

    Examples:
        >>> MarkdownToPdfPipeline.default().__class__.__name__
        'MarkdownToPdfPipeline'
    """

    @classmethod
    def default(cls) -> MarkdownToPdfPipeline:
        """Create a default pipeline.

        Args:
            None.

        Returns:
            Pipeline instance.

        Raises:
            None.

        Examples:
            >>> isinstance(MarkdownToPdfPipeline.default(), MarkdownToPdfPipeline)
            True
        """
        return cls()

    def render_html(
        self,
        source: MarkdownSource,
        options: RenderOptions | None = None,
    ) -> StyledHtmlDocument:
        """Render Markdown source to styled HTML.

        Args:
            source: Markdown source.
            options: Render options.

        Returns:
            Styled HTML document.

        Raises:
            ValueError: If an unknown engine is configured.

        Examples:
            >>> source = MarkdownSource.from_text('# Hello')
            >>> MarkdownToPdfPipeline.default().render_html(source)  # doctest: +SKIP
        """
        resolved = options or RenderOptions()
        configure_logging(resolved.logging)
        logger = get_logger(__name__)
        logger.info("render_html.started", extra={"source_kind": source.kind})

        parsed = FrontmatterParser().parse(source)
        resolved = self._apply_metadata_options(parsed.metadata, resolved)

        engine = self._markdown_engine(resolved.markdown_engine)
        html_doc = engine.render(parsed, resolved)
        styled = HtmlBuilder().build(html_doc, resolved)

        self._write_debug_artifacts(styled, resolved)
        logger.info("render_html.finished", extra={"theme": resolved.theme})
        return styled

    def render(self, source: MarkdownSource, options: RenderOptions | None = None) -> PdfArtifact:
        """Render Markdown source to a PDF artifact.

        Args:
            source: Markdown source.
            options: Render options.

        Returns:
            PDF artifact.

        Raises:
            ValueError: If an unknown renderer is configured.

        Examples:
            >>> source = MarkdownSource.from_text('# Hello')
            >>> MarkdownToPdfPipeline.default().render(source)  # doctest: +SKIP
        """
        resolved = options or RenderOptions()
        configure_logging(resolved.logging)
        logger = get_logger(__name__)
        logger.info("render.started", extra={"source_kind": source.kind})

        styled = self.render_html(source, resolved)
        artifact = self._pdf_renderer(resolved.engine).render(styled, resolved)
        if resolved.output is not None:
            artifact = self.write_artifact(artifact, resolved.output)
        logger.info(
            "render.finished",
            extra={"engine": resolved.engine, "output": str(artifact.output_path or "")},
        )
        return artifact

    def write_artifact(self, artifact: PdfArtifact, output: str | Path) -> PdfArtifact:
        """Write a PDF artifact to disk.

        Args:
            artifact: PDF artifact.
            output: Output path.

        Returns:
            Updated PDF artifact with ``output_path`` populated.

        Raises:
            OSError: If the output cannot be written.

        Examples:
            >>> artifact = PdfArtifact(content=b'%PDF-demo')
            >>> MarkdownToPdfPipeline.default().write_artifact(artifact, 'x.pdf')  # doctest: +SKIP
        """
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(artifact.content)
        return artifact.model_copy(update={"output_path": path})

    def _apply_metadata_options(
        self,
        metadata: dict[str, Any],
        options: RenderOptions,
    ) -> RenderOptions:
        """Apply profile and frontmatter metadata to options.

        Args:
            metadata: Parsed frontmatter metadata.
            options: Current render options.

        Returns:
            Render options with metadata defaults applied conservatively.

        Raises:
            None.
        """
        profile_name = str(metadata.get("profile") or options.profile)
        profile_defaults = (
            get_profile_defaults(profile_name) if profile_name in self._profile_names() else {}
        )
        candidate: dict[str, Any] = {**profile_defaults, **metadata}
        allowed = set(RenderOptions.model_fields)
        updates = {key: value for key, value in candidate.items() if key in allowed}
        # Keep explicit output/source/path fields from the caller untouched.
        for protected in {"source", "output", "out_dir", "paths", "logging"}:
            updates.pop(protected, None)
        return options.model_copy(update=updates)

    def _write_debug_artifacts(self, styled: StyledHtmlDocument, options: RenderOptions) -> None:
        """Write debug HTML/CSS artifacts when requested.

        Args:
            styled: Styled HTML document.
            options: Render options.

        Returns:
            None.

        Raises:
            OSError: If debug files cannot be written.
        """
        if options.debug_html:
            target = self._debug_path(options, suffix=".html")
            target.write_text(styled.html, encoding="utf-8")
        if options.debug_css:
            target = self._debug_path(options, suffix=".css")
            target.write_text(styled.css, encoding="utf-8")

    def _debug_path(self, options: RenderOptions, *, suffix: str) -> Path:
        """Build a debug artifact path.

        Args:
            options: Render options.
            suffix: Debug file suffix.

        Returns:
            Debug artifact path.

        Raises:
            None.
        """
        output = options.output or Path("markprint-output.pdf")
        path = output.with_suffix(suffix)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

    def _markdown_engine(self, name: str) -> object:
        if name == "markdown-it":
            return MarkdownItEngine()
        if name == "python-markdown":
            return PythonMarkdownEngine()
        if name == "pandoc":
            return PandocMarkdownEngine()
        raise ValueError(f"Unknown Markdown engine: {name}")

    def _pdf_renderer(self, name: str) -> object:
        if name == "weasyprint":
            return WeasyPrintRenderer()
        if name == "playwright":
            return PlaywrightRenderer()
        if name == "pandoc":
            return PandocRenderer()
        raise ValueError(f"Unknown PDF renderer: {name}")

    def _profile_names(self) -> set[str]:
        """Return known built-in profile names.

        Args:
            None.

        Returns:
            Built-in profile names.

        Raises:
            None.
        """
        from markprint.config.profiles import list_profiles

        return set(list_profiles())
