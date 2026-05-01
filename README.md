# Markprint

Beautiful, configurable, extensible Markdown-to-PDF rendering for Python.

Markprint is designed as a real document compiler rather than a tiny conversion script. It accepts files, raw Markdown strings, stdin, batches, or multi-file manuals; renders Markdown into themed printable HTML; then converts that HTML into PDF through WeasyPrint by default, with optional Playwright and Pandoc backends for browser-rendered diagrams/math and academic workflows.

## Highlights

- File input: `markprint README.md README.pdf`
- Inferred output: `markprint README.md`
- Raw string input: `markprint render-string "# Hello" --output hello.pdf`
- Stdin input: `echo "# Hello" | markprint - hello.pdf`
- Batch render: `markprint batch docs/*.md --out-dir dist/pdf`
- Compile mode: `markprint compile docs/intro.md docs/usage.md --output manual.pdf`
- Built-in themes: default, GitHub, Nord, Dracula, report, resume, academic
- Built-in profiles: docs, report, resume, academic, book, whitepaper
- Markdown frontmatter configuration
- `pyproject.toml`, `markprint.toml`, and `.markprint.toml` discovery
- Typer CLI with Rich output
- Pydantic v2 settings models
- Pygments code highlighting
- Optional `ultilog` logging backend
- Optional Playwright, Pandoc, Python-Markdown, pypdf, pikepdf, and PyMuPDF extension points

## Installation

```bash
pdm add markprint
```

From this repository:

```bash
pdm install -G dev -G test -G docs
pdm run markprint README.md README.pdf
```

Full local development install:

```bash
pdm install -G all
pdm run playwright install chromium
```

## Quickstart

```bash
markprint README.md README.pdf
markprint README.md --theme github --toc
markprint render-string "# Hello\n\nThis is **Markdown**." --output hello.pdf
cat README.md | markprint - README.pdf
```

## Python API

```python
from pathlib import Path

from markprint import RenderOptions, render_pdf

artifact = render_pdf(
    markdown="# Hello\n\nThis is **raw Markdown**.",
    output=Path("hello.pdf"),
    options=RenderOptions(theme="github", toc=True),
)

print(artifact.output_path)
```

## Configuration

Markprint reads configuration from:

1. CLI flags
2. Python API `RenderOptions`
3. Markdown frontmatter
4. `markprint.toml`, `.markprint.toml`, or `[tool.markprint]` in `pyproject.toml`
5. Built-in defaults

Example:

```toml
[tool.markprint]
default_input = "README.md"
default_output = "dist/README.pdf"
engine = "weasyprint"
markdown_engine = "markdown-it"
theme = "github"
profile = "docs"
toc = true
page_numbers = true
code_theme = "default"
page_size = "Letter"
margin = "0.8in"

[tool.markprint.logging]
enabled = true
backend = "ultilog"
preset = "dev"
level = "INFO"
mode = "rich"
```

Frontmatter example:

```markdown
---
title: Architecture Report
profile: report
theme: nord
toc: true
page_numbers: true
---

# Overview
```

## CLI reference

```bash
markprint [INPUT] [OUTPUT]
markprint render INPUT [OUTPUT]
markprint render-string MARKDOWN --output OUTPUT
markprint batch INPUTS... --out-dir DIR
markprint compile INPUTS... --output OUTPUT
markprint html INPUT --output OUTPUT.html
markprint themes
markprint profiles
markprint engines
markprint config
markprint doctor
```

## Architecture

```text
MarkdownSource
  → FrontmatterParser
  → MarkdownEngine
  → HtmlDocument
  → HtmlBuilder + ThemeRegistry + Pygments
  → StyledHtmlDocument
  → PdfRenderer
  → PdfArtifact
```

Strict boundaries keep the package extensible:

- Markdown engines never know about PDF rendering.
- PDF renderers never know about Markdown syntax.
- Themes only provide templates and CSS.
- Logging is optional and adapter-based.
- Heavy dependencies live behind extras.

## Testing

```bash
pdm run pytest
pdm run pytest --cov=markprint --cov-report=term-missing
```

The repository includes unit, integration, e2e, and visual test scaffolds.

## Optional extras

```bash
pdm add "markprint[logging]"        # ultilog
pdm add "markprint[browser]"        # Playwright
pdm add "markprint[pandoc]"         # pypandoc
pdm add "markprint[markdown-python]"# Python-Markdown + pymdown-extensions
pdm add "markprint[pdf]"            # pypdf, pikepdf, PyMuPDF
pdm add "markprint[all]"            # everything
```

## Development roadmap

- Strengthen config precedence and theme inheritance
- Add more Markdown plugins and custom admonitions
- Add Mermaid pre-render mode
- Add MathJax/KaTeX browser rendering
- Add Pandoc citation workflows
- Add PDF metadata/merge/preview commands
- Add plugin discovery through entry points
- Add visual regression fixtures

## License

MIT
