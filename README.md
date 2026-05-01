# Markprint

[![PyPI](https://img.shields.io/pypi/v/markprint.svg)](https://pypi.org/project/markprint/)
[![Python](https://img.shields.io/pypi/pyversions/markprint.svg)](https://pypi.org/project/markprint/)
[![CI](https://github.com/pr1m8/markprint/actions/workflows/ci.yml/badge.svg)](https://github.com/pr1m8/markprint/actions/workflows/ci.yml)
[![Release](https://github.com/pr1m8/markprint/actions/workflows/release.yml/badge.svg)](https://github.com/pr1m8/markprint/actions/workflows/release.yml)
[![Docs](https://readthedocs.org/projects/markprint/badge/?version=latest)](https://markprint.readthedocs.io/en/latest/)
[![License](https://img.shields.io/github/license/pr1m8/markprint.svg)](LICENSE)

**Markprint** is a beautiful, configurable, extensible Markdown-to-PDF renderer for Python.

It is built for developers who want polished PDFs from Markdown without giving up control over themes, profiles, syntax highlighting, document metadata, batch rendering, logging, or advanced rendering backends.

```text
Markdown source
  -> frontmatter and config
  -> parsed document model
  -> HTML body
  -> themed printable HTML
  -> PDF artifact
```

## Why Markprint?

Markdown-to-PDF tooling often falls into two extremes. Some tools are easy but plain. Others are powerful but heavy, requiring Pandoc, LaTeX, browser automation, or lots of project-specific glue. Markprint aims for a better middle path:

- simple by default,
- beautiful out of the box,
- deeply configurable when needed,
- extensible through clean rendering stages,
- useful as both a CLI and Python library.

## Installation

```bash
pip install markprint
```

With optional extras:

```bash
pip install "markprint[logging]"
pip install "markprint[browser]"
pip install "markprint[pandoc]"
pip install "markprint[pdf]"
```

For local development:

```bash
pdm install -G dev -G test -G docs
```

## Quickstart

Render a Markdown file to PDF:

```bash
markprint README.md README.pdf
```

Render raw Markdown:

```bash
markprint render-string "# Hello Markprint" --output hello.pdf
```

Render from stdin:

```bash
echo "# Hello from stdin" | markprint - hello.pdf
```

Compile multiple Markdown files into one PDF:

```bash
markprint compile docs/intro.md docs/usage.md docs/api.md --output manual.pdf
```

## Python API

```python
from pathlib import Path

from markprint import RenderOptions, render_pdf

render_pdf(
    source=Path("README.md"),
    output=Path("README.pdf"),
    options=RenderOptions(theme="github", profile="docs", toc=True),
)
```

Raw Markdown:

```python
from markprint import render_pdf

render_pdf(
    markdown="# Hello

This is **raw Markdown**.",
    output="hello.pdf",
)
```

## Documentation

- Documentation: https://markprint.readthedocs.io/
- PyPI: https://pypi.org/project/markprint/
- Repository: https://github.com/pr1m8/markprint

## Core features

- Markdown file, raw string, stdin, batch, and multi-file input
- YAML frontmatter and project config support
- Themeable Jinja HTML templates
- Pygments syntax highlighting
- WeasyPrint backend by default
- Optional Playwright and Pandoc backends
- Optional ultilog logging integration
- PDF helper extension points
- Plugin-oriented architecture

## Development

```bash
pdm install -G dev -G test -G docs
pdm run ruff check .
pdm run ruff format --check .
pdm run pytest --cov=markprint --cov-report=term-missing
pdm run mkdocs build --strict
```

## License

MIT.
