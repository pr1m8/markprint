"""Path resolution helpers for Markprint."""

from __future__ import annotations

from pathlib import Path


def infer_output_path(source_path: Path, *, out_dir: Path | None = None) -> Path:
    """Infer a PDF output path from a Markdown source path.

    Args:
        source_path: Input Markdown path.
        out_dir: Optional output directory.

    Returns:
        Inferred PDF output path.

    Raises:
        None.

    Examples:
        >>> infer_output_path(Path("README.md"))
        PosixPath('README.pdf')
    """
    filename = source_path.with_suffix(".pdf").name
    return (out_dir / filename) if out_dir is not None else source_path.with_suffix(".pdf")
