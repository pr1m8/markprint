# Quickstart

## Render a file

```bash
markprint README.md README.pdf
```

## Infer the output name

```bash
markprint README.md
```

This writes `README.pdf`.

## Render a raw Markdown string

```bash
markprint render-string "# Hello Markprint" --output hello.pdf
```

## Render from stdin

```bash
echo "# Hello from stdin" | markprint - hello.pdf
```

## Add a theme

```bash
markprint README.md README.pdf --theme github
```

## Add a profile

```bash
markprint report.md report.pdf --profile report --theme nord --toc
```

## Add frontmatter

```markdown
---
title: Architecture Report
author: William R. Astley
theme: nord
profile: report
toc: true
page_numbers: true
---

# Overview
```

Then run:

```bash
markprint report.md report.pdf
```

## Use Python

```python
from markprint import RenderOptions, render_pdf

render_pdf(
    markdown="# Hello

This came from Python.",
    output="hello.pdf",
    options=RenderOptions(theme="github", toc=True),
)
```
