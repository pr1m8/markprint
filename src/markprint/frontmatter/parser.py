"""Frontmatter parsing for Markprint.

Purpose:
    Split YAML-like frontmatter from Markdown content.

Examples:
    >>> from markprint.sources.models import MarkdownSource
    >>> parser = FrontmatterParser()
    >>> doc = parser.parse(MarkdownSource.from_text("---\ntitle: Hi\n---\n# Body"))
    >>> doc.metadata["title"]
    'Hi'
"""

from __future__ import annotations

from typing import Any

from markprint.document.models import ParsedDocument
from markprint.sources.models import MarkdownSource


class FrontmatterParser:
    """Parse frontmatter from Markdown sources."""

    def parse(self, source: MarkdownSource) -> ParsedDocument:
        """Parse a Markdown source.

        Args:
            source: Loaded Markdown source.

        Returns:
            Parsed document with body and metadata.

        Raises:
            None.

        Examples:
            >>> from markprint.sources.models import MarkdownSource
            >>> FrontmatterParser().parse(MarkdownSource.from_text("# Hi")).body_markdown
            '# Hi'
        """
        try:
            import frontmatter
        except ImportError:
            metadata, body = self._parse_simple(source.text)
        else:
            post = frontmatter.loads(source.text)
            metadata, body = dict(post.metadata), post.content
        return ParsedDocument(
            body_markdown=body,
            metadata=metadata,
            source_path=source.path,
            base_dir=source.base_dir,
        )

    def _parse_simple(self, text: str) -> tuple[dict[str, Any], str]:
        """Parse a tiny YAML-like frontmatter subset.

        Args:
            text: Markdown text.

        Returns:
            Metadata dictionary and Markdown body.

        Raises:
            None.

        Examples:
            >>> FrontmatterParser()._parse_simple("---\ntitle: Hi\n---\n# Body")[0]["title"]
            'Hi'
        """
        if not text.startswith("---\n"):
            return {}, text
        end = text.find("\n---", 4)
        if end == -1:
            return {}, text
        raw = text[4:end].strip()
        body = text[text.find("\n", end + 1) + 1 :]
        metadata: dict[str, Any] = {}
        for line in raw.splitlines():
            if ":" not in line:
                continue
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"\'')
        return metadata, body
