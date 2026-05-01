# Your First PDF

Create `hello.md`:

````markdown
---
title: Hello Markprint
theme: github
toc: true
---

# Hello

This is my first **Markprint** PDF.

```python
print("hello from a code block")
```
````

Render it:

```bash
markprint hello.md hello.pdf
```

## What happened?

Markprint performed these steps:

1. Loaded `hello.md`.
2. Parsed frontmatter.
3. Converted Markdown to HTML.
4. Generated syntax highlighting CSS.
5. Loaded the `github` theme.
6. Built a full printable HTML document.
7. Rendered the PDF.

## Debug the intermediate HTML

```bash
markprint hello.md hello.pdf --debug-html --debug-css
```

Use debug output when a theme, asset, or layout does not look right.
