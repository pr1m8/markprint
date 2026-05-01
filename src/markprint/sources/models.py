"""Document source models for Markprint.

Purpose:
    Represent Markdown input from files, raw strings, stdin, and compiled
    multi-file sources.

Design:
    All source modes normalize into ``MarkdownSource`` so downstream pipeline
    stages do not care where text came from.

Examples:
    >>> source = MarkdownSource.from_text("# Hello", virtual_path="inline.md")
    >>> source.kind
    'string'
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field


class MarkdownSource(BaseModel):
    """Loaded Markdown source.

    Args:
        text: Markdown text.
        path: Real or virtual source path.
        base_dir: Base directory used to resolve relative assets.
        kind: Source origin kind.

    Returns:
        A normalized Markdown source model.

    Raises:
        pydantic.ValidationError: If source data is invalid.

    Examples:
        >>> source = MarkdownSource.from_text("# Hello", virtual_path="inline.md")
        >>> source.text
        '# Hello'
    """

    model_config = ConfigDict(extra="forbid")

    text: str
    path: Path | None = None
    base_dir: Path = Field(default_factory=Path.cwd)
    kind: Literal["file", "string", "stdin", "compiled"] = "file"

    @classmethod
    def from_text(
        cls,
        text: str,
        *,
        virtual_path: str | Path = "inline.md",
        base_dir: str | Path | None = None,
    ) -> Self:
        """Create a Markdown source from raw text.

        Args:
            text: Raw Markdown text.
            virtual_path: Virtual path used for diagnostics and naming.
            base_dir: Base directory for resolving relative assets.

        Returns:
            A Markdown source with ``kind='string'``.

        Raises:
            pydantic.ValidationError: If model validation fails.

        Examples:
            >>> MarkdownSource.from_text("# Hello").kind
            'string'
        """
        return cls(
            text=text,
            path=Path(virtual_path),
            base_dir=Path(base_dir) if base_dir is not None else Path.cwd(),
            kind="string",
        )

    @classmethod
    def from_file(cls, path: str | Path) -> Self:
        """Create a Markdown source from a file.

        Args:
            path: Markdown file path.

        Returns:
            A Markdown source loaded from disk.

        Raises:
            FileNotFoundError: If the file does not exist.
            UnicodeDecodeError: If the file cannot be decoded as UTF-8.

        Examples:
            >>> source = MarkdownSource.from_file("README.md")  # doctest: +SKIP
            >>> source.kind
            'file'
        """
        source_path = Path(path)
        return cls(
            text=source_path.read_text(encoding="utf-8"),
            path=source_path,
            base_dir=source_path.parent,
            kind="file",
        )

    @classmethod
    def from_stdin(cls, text: str, *, base_dir: str | Path | None = None) -> Self:
        """Create a Markdown source from stdin text.

        Args:
            text: Markdown text read from stdin.
            base_dir: Base directory for resolving relative assets.

        Returns:
            A Markdown source with ``kind='stdin'``.

        Raises:
            pydantic.ValidationError: If model validation fails.

        Examples:
            >>> MarkdownSource.from_stdin("# Hello").kind
            'stdin'
        """
        return cls(
            text=text,
            path=Path("stdin.md"),
            base_dir=Path(base_dir) if base_dir is not None else Path.cwd(),
            kind="stdin",
        )

    @classmethod
    def compile_files(cls, paths: list[str | Path]) -> Self:
        """Compile multiple Markdown files into one source.

        Args:
            paths: Markdown files in document order.

        Returns:
            A compiled Markdown source.

        Raises:
            FileNotFoundError: If any file is missing.
            UnicodeDecodeError: If any file cannot be decoded.

        Examples:
            >>> MarkdownSource.compile_files(["a.md", "b.md"])  # doctest: +SKIP
        """
        resolved = [Path(path) for path in paths]
        text = "\n\n".join(path.read_text(encoding="utf-8") for path in resolved)
        base_dir = resolved[0].parent if resolved else Path.cwd()
        return cls(text=text, path=Path("compiled.md"), base_dir=base_dir, kind="compiled")
