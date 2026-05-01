# Markprint

**Markprint** is a beautiful, configurable, extensible Markdown-to-PDF renderer for Python.

It is designed for the common case where you already have Markdown - notes, READMEs, architecture reports, resumes, technical docs, generated AI reports, internal specs - and you want a polished PDF without building a custom document pipeline from scratch.

<div class="grid cards" markdown>

-   :material-file-document-edit:{ .lg .middle } **Markdown in**

    ---

    Files, raw strings, stdin, batches, and multi-file manuals.

-   :material-palette:{ .lg .middle } **Beautiful output**

    ---

    Themes, profiles, syntax highlighting, frontmatter, and print-aware layout.

-   :material-language-python:{ .lg .middle } **Python first**

    ---

    Use it as a CLI or import it into your own code.

-   :material-puzzle:{ .lg .middle } **Extensible**

    ---

    Renderer, theme, PDF, logging, and plugin extension points.

</div>

## The shortest path

```bash
pip install markprint
markprint README.md README.pdf
```

That command reads `README.md`, converts it to themed HTML, and renders a PDF.

## What Markprint is good for

Markprint is best when you want Markdown authoring plus reliable document output:

- project READMEs exported to PDF,
- internal technical reports,
- architecture decision records,
- resume drafts,
- client-facing proposals,
- generated AI research notes,
- multi-file manuals,
- reproducible docs pipelines.

## Mental model

```text
Markdown source
  -> source loader
  -> frontmatter parser
  -> Markdown engine
  -> document model
  -> HTML builder
  -> theme resolver
  -> PDF renderer
  -> PDF artifact
```

Markprint separates each step so the package can stay simple on the surface while still supporting advanced use cases.

## Quick examples

Render a Markdown file:

```bash
markprint README.md README.pdf
```

Render raw Markdown:

```bash
markprint render-string "# Hello" --output hello.pdf
```

Render from stdin:

```bash
echo "# Hello" | markprint - hello.pdf
```

Compile multiple Markdown files into one PDF:

```bash
markprint compile docs/intro.md docs/usage.md docs/api.md --output manual.pdf
```

Use from Python:

```python
from markprint import render_pdf

render_pdf(markdown="# Hello

Rendered from Python.", output="hello.pdf")
```

## Where to go next

- New user? Start with [Quickstart](getting-started/quickstart.md).
- Want to understand the design? Read [Architecture](concepts/architecture.md).
- Need all CLI options? See [CLI Reference](reference/cli.md).
- Need a Python integration? See [Python API](reference/python-api.md).
- Publishing docs? See [Release](development/release.md).
