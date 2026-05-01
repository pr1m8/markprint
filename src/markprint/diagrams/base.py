"""Diagram rendering protocols."""
from __future__ import annotations
from typing import Protocol
class DiagramRenderer(Protocol):
    """Render diagram code to embeddable assets."""
    def render_svg(self, code: str) -> str:
        """Render diagram code to SVG.

        Args:
            code: Diagram source.

        Returns:
            SVG markup.
        """
        ...
