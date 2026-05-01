"""Document metadata helpers."""
from __future__ import annotations
def get_title(metadata: dict[str, object], fallback: str = "Untitled") -> str:
    """Read a title from metadata.

    Args:
        metadata: Document metadata.
        fallback: Fallback title.

    Returns:
        Title string.

    Raises:
        None.

    Examples:
        >>> get_title({'title': 'Hi'})
        'Hi'
    """
    value = metadata.get("title", fallback)
    return str(value)
