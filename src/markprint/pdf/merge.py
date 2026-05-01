"""PDF merge helpers using optional pypdf."""
from __future__ import annotations
from pathlib import Path
from markprint.diagnostics.errors import DependencyMissingError
def merge_pdfs(paths: list[Path], output: Path) -> Path:
    """Merge PDFs using pypdf.

    Args:
        paths: Input PDF paths.
        output: Output path.

    Returns:
        Output path.

    Raises:
        DependencyMissingError: If pypdf is missing.
    """
    try:
        from pypdf import PdfWriter
    except ImportError as exc:
        raise DependencyMissingError("Install with: pip install 'markprint[pdf]'") from exc
    writer = PdfWriter()
    for path in paths:
        writer.append(str(path))
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("wb") as handle:
        writer.write(handle)
    return output
