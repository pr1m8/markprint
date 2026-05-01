"""PDF preview helpers using optional PyMuPDF."""

from __future__ import annotations

from pathlib import Path

from markprint.diagnostics.errors import DependencyMissingError


def render_first_page(pdf_path: Path, output_path: Path) -> Path:
    """Render the first page of a PDF to PNG.

    Args:
        pdf_path: Source PDF path.
        output_path: Output PNG path.

    Returns:
        Output PNG path.

    Raises:
        DependencyMissingError: If PyMuPDF is missing.
    """
    try:
        import fitz
    except ImportError as exc:
        raise DependencyMissingError("Install with: pip install 'markprint[pdf]'") from exc
    doc = fitz.open(pdf_path)
    pix = doc[0].get_pixmap()
    pix.save(output_path)
    return output_path
