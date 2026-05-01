"""Beautiful, configurable Markdown-to-PDF rendering.

Purpose:
    Expose the public Markprint API with lazy imports so optional rendering
    dependencies are not imported until they are needed.

Design:
    Lightweight models are exported directly. Rendering helpers are resolved
    lazily through ``__getattr__``.

Attributes:
    __version__: Package version.

Examples:
    >>> from markprint import RenderOptions
    >>> RenderOptions().engine
    'weasyprint'
"""

from __future__ import annotations

from markprint.api import (
    list_profiles,
    list_themes,
    render_html,
    render_pdf,
    render_pdf_bytes,
)
from markprint.config.models import LoggingSettings, RenderOptions
from markprint.document.models import PdfArtifact
from markprint.sources.models import MarkdownSource

__version__ = "0.1.0"

_LAZY_API = {
    "list_profiles",
    "list_themes",
    "render_html",
    "render_pdf",
    "render_pdf_bytes",
}


def __getattr__(name: str) -> object:
    """Resolve rendering helpers lazily.

    Args:
        name: Attribute name.

    Returns:
        Requested public API attribute.

    Raises:
        AttributeError: If the name is not public.

    Examples:
        >>> callable(__getattr__("render_html"))
        True
    """
    if name in _LAZY_API:
        from markprint import api

        return getattr(api, name)
    raise AttributeError(name)


__all__ = [
    "LoggingSettings",
    "MarkdownSource",
    "PdfArtifact",
    "RenderOptions",
    "list_profiles",
    "list_themes",
    "render_html",
    "render_pdf",
    "render_pdf_bytes",
]
