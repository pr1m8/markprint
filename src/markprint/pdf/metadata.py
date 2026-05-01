"""PDF metadata helpers."""
from __future__ import annotations
from markprint.document.models import PdfArtifact
def with_metadata(artifact: PdfArtifact, metadata: dict[str, str]) -> PdfArtifact:
    """Attach metadata to an artifact model.

    Args:
        artifact: PDF artifact.
        metadata: Metadata dictionary.

    Returns:
        Updated artifact model.

    Raises:
        None.
    """
    return artifact.model_copy(update={"metadata": metadata})
