# Getting Started

This section takes you from installation to your first PDF and then into the workflows Markprint is designed to support.

## Recommended path

1. Install Markprint.
2. Render a single Markdown file.
3. Add frontmatter.
4. Choose a theme/profile.
5. Add config to `pyproject.toml`.
6. Use batch or compile mode as needed.

## Basic workflow

```bash
markprint README.md README.pdf
```

## Python workflow

```python
from markprint import render_pdf

render_pdf(markdown="# Hello", output="hello.pdf")
```

## Project workflow

```toml
[tool.markprint]
theme = "github"
profile = "docs"
toc = true
page_numbers = true
```

Then:

```bash
markprint README.md README.pdf
```
