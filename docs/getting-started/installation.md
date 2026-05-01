# Installation

## Basic install

```bash
pip install markprint
```

## Development install

If you are working on the repository itself:

```bash
pdm install -G dev -G test -G docs
```

## Optional extras

Markprint keeps heavyweight dependencies optional.

```bash
pip install "markprint[logging]"
pip install "markprint[browser]"
pip install "markprint[pandoc]"
pip install "markprint[pdf]"
```

## Extras explained

| Extra | Purpose |
|---|---|
| `logging` | Optional `ultilog` integration |
| `browser` | Playwright-based rendering for browser-dependent documents |
| `pandoc` | Pandoc backend for academic/document workflows |
| `pdf` | PDF helpers such as merge, preview, metadata, and inspection |
| `docs` | MkDocs documentation tooling |
| `test` | Pytest and coverage tools |
| `dev` | Build, lint, format, release utilities |

## WeasyPrint note

The default backend uses WeasyPrint. Most modern Python environments install it cleanly, but some Linux systems may need system packages for fonts and rendering libraries. If PDF rendering fails at runtime, run:

```bash
markprint doctor
```

and inspect the missing dependency message.
