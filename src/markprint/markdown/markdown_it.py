"""Default Markdown engine with a safe built-in fallback.

Purpose:
    Render common Markdown to HTML without requiring heavy optional imports at
    module import time.
"""
from __future__ import annotations

import html
import re

from markprint.config.models import RenderOptions
from markprint.document.headings import extract_headings
from markprint.document.models import HtmlDocument, ParsedDocument


class MarkdownItEngine:
    """Render Markdown into a small, useful HTML subset.

    Args:
        None.

    Returns:
        A Markdown engine instance.

    Raises:
        None.

    Examples:
        >>> engine = MarkdownItEngine()
        >>> engine.name
        'markdown-it'
    """

    name = "markdown-it"

    def render(self, document: ParsedDocument, options: RenderOptions) -> HtmlDocument:
        """Render Markdown to HTML.

        Args:
            document: Parsed Markdown document.
            options: Render options.

        Returns:
            Rendered HTML document.

        Raises:
            None.
        """
        html_body = _render_basic_markdown(document.body_markdown)
        headings = extract_headings(document.body_markdown)
        return HtmlDocument(
            body_html=html_body,
            metadata=document.metadata,
            headings=headings,
            base_url=document.base_dir,
        )


def _render_basic_markdown(markdown: str) -> str:
    """Render a pragmatic Markdown subset to HTML.

    Args:
        markdown: Markdown text.

    Returns:
        HTML string.

    Raises:
        None.
    """
    blocks: list[str] = []
    paragraph: list[str] = []
    in_code = False
    code_lang = ""
    code_lines: list[str] = []

    def flush_paragraph() -> None:
        if paragraph:
            text = " ".join(part.strip() for part in paragraph).strip()
            blocks.append(f"<p>{_inline(text)}</p>")
            paragraph.clear()

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code:
                code = html.escape("\n".join(code_lines))
                lang_class = f' class="language-{html.escape(code_lang)}"' if code_lang else ""
                blocks.append(f"<pre><code{lang_class}>{code}</code></pre>")
                in_code = False
                code_lang = ""
                code_lines.clear()
            else:
                flush_paragraph()
                in_code = True
                code_lang = line[3:].strip()
            continue
        if in_code:
            code_lines.append(raw_line)
            continue
        if not line.strip():
            flush_paragraph()
            continue
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            flush_paragraph()
            level = len(match.group(1))
            text = match.group(2).strip()
            slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
            blocks.append(f'<h{level} id="{html.escape(slug)}">{_inline(text)}</h{level}>')
            continue
        if line.startswith("- "):
            flush_paragraph()
            blocks.append(f"<ul><li>{_inline(line[2:].strip())}</li></ul>")
            continue
        paragraph.append(line)
    flush_paragraph()
    if in_code:
        code = html.escape("\n".join(code_lines))
        blocks.append(f"<pre><code>{code}</code></pre>")
    return "\n".join(blocks)


def _inline(text: str) -> str:
    """Render simple inline Markdown spans.

    Args:
        text: Inline Markdown text.

    Returns:
        Escaped HTML with simple emphasis/link/image spans.

    Raises:
        None.
    """
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img alt="\1" src="\2" />', escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped
