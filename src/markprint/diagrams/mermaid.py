"""Mermaid rendering placeholders."""

from __future__ import annotations

from markprint.diagnostics.errors import DependencyMissingError


class MermaidRenderer:
    """Future Mermaid renderer using Playwright or Mermaid CLI."""

    def render_svg(self, code: str) -> str:
        """Render Mermaid to SVG.

        Args:
            code: Mermaid diagram code.

        Returns:
            SVG markup.

        Raises:
            DependencyMissingError: Always until backend implementation is selected.
        """
        raise DependencyMissingError("Mermaid rendering is planned for markprint[browser].")
