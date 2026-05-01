# Configuration

Markprint supports `markprint.toml`, `.markprint.toml`, and `[tool.markprint]` in `pyproject.toml`.

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
enabled = false
backend = "stdlib"
level = "INFO"
```

## Precedence

1. CLI flags
2. Python API options
3. Markdown frontmatter
4. Project config
5. Built-in defaults
