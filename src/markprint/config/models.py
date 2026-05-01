"""Configuration models for Markprint.

Purpose:
    Define validated render and logging options shared by the CLI, Python API,
    configuration files, and tests.

Design:
    Models describe user intent rather than backend implementation details.
    Renderer-specific options can be added as nested models without changing
    the public API shape.

Examples:
    >>> options = RenderOptions(theme="github", toc=True)
    >>> options.theme
    'github'
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class LoggingSettings(BaseModel):
    """Logging configuration.

    Args:
        enabled: Whether Markprint should configure logging.
        backend: Logging backend.
        preset: Logging preset.
        level: Logging level.
        mode: Output mode for logging.
        force: Whether to force reconfiguration.

    Returns:
        A validated logging settings model.

    Raises:
        pydantic.ValidationError: If fields are invalid.

    Examples:
        >>> settings = LoggingSettings(enabled=True, backend="ultilog")
        >>> settings.backend
        'ultilog'
    """

    model_config = ConfigDict(extra="forbid")

    enabled: bool = False
    backend: Literal["stdlib", "ultilog"] = "stdlib"
    preset: Literal["dev", "test", "prod"] = "dev"
    level: str = "INFO"
    mode: Literal["rich", "plain", "json"] = "rich"
    force: bool = False


class PathSettings(BaseModel):
    """Filesystem defaults for rendering.

    Args:
        default_input: Optional default Markdown input path.
        default_output: Optional default PDF output path.
        default_out_dir: Optional default batch output directory.
        assets_dir: Optional directory for shared assets.
        themes_dir: Optional custom themes directory.
        templates_dir: Optional custom templates directory.

    Returns:
        A validated path settings model.

    Raises:
        pydantic.ValidationError: If paths are invalid.

    Examples:
        >>> settings = PathSettings(default_input="README.md")
        >>> str(settings.default_input)
        'README.md'
    """

    default_input: Path | None = None
    default_output: Path | None = None
    default_out_dir: Path | None = None
    assets_dir: Path | None = None
    themes_dir: Path | None = None
    templates_dir: Path | None = None


class RenderOptions(BaseModel):
    """Options for a Markdown-to-PDF render operation.

    Args:
        source: Optional input Markdown file.
        output: Optional output PDF path.
        out_dir: Optional output directory for batch jobs.
        base_url: Base directory for relative assets.
        engine: PDF rendering backend.
        markdown_engine: Markdown parser backend.
        theme: Theme name or path.
        profile: Document profile.
        toc: Whether to generate a table of contents.
        page_numbers: Whether to render page numbers.
        code_theme: Syntax highlighting theme.
        page_size: CSS page size.
        margin: CSS page margin.
        debug_html: Whether to write intermediate HTML.
        debug_css: Whether to write intermediate CSS.
        open_after_render: Whether to open the PDF after rendering.
        logging: Logging settings.
        paths: Path defaults.

    Returns:
        A validated render options model.

    Raises:
        pydantic.ValidationError: If options are invalid.

    Examples:
        >>> options = RenderOptions(theme="nord", page_numbers=True)
        >>> options.theme
        'nord'
    """

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)

    source: Path | None = None
    output: Path | None = None
    out_dir: Path | None = None
    base_url: Path | None = None

    engine: Literal["weasyprint", "playwright", "pandoc"] = "weasyprint"
    markdown_engine: Literal["markdown-it", "python-markdown", "pandoc"] = "markdown-it"

    theme: str = "default"
    profile: str = "docs"

    toc: bool = False
    page_numbers: bool = True
    code_theme: str = "default"

    page_size: str = "Letter"
    margin: str = "0.8in"

    debug_html: bool = False
    debug_css: bool = False
    open_after_render: bool = False

    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    paths: PathSettings = Field(default_factory=PathSettings)

    @model_validator(mode="after")
    def validate_output_targets(self) -> "RenderOptions":
        """Validate mutually exclusive output choices.

        Args:
            None.

        Returns:
            The validated model.

        Raises:
            ValueError: If both ``output`` and ``out_dir`` are invalidly combined.

        Examples:
            >>> RenderOptions(output="a.pdf").output.name
            'a.pdf'
        """
        if self.output is not None and self.out_dir is not None:
            raise ValueError("Use either output or out_dir for a single render, not both.")
        return self

    def with_output_default(self, source_path: Path | None = None) -> "RenderOptions":
        """Return options with an inferred PDF output if missing.

        Args:
            source_path: Optional path used to infer the output name.

        Returns:
            A copied options model with ``output`` populated when possible.

        Raises:
            ValueError: If no output can be inferred.

        Examples:
            >>> RenderOptions().with_output_default(Path("README.md")).output.name
            'README.pdf'
        """
        if self.output is not None:
            return self
        candidate = source_path or self.source or self.paths.default_input
        if candidate is None:
            raise ValueError("No output path provided and no source path available for inference.")
        output = candidate.with_suffix(".pdf")
        return self.model_copy(update={"output": output})
