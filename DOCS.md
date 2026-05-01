# Documentation Guide

This repository uses MkDocs Material for the public documentation site.

## Local docs workflow

```bash
pdm install -G docs
pdm run mkdocs serve
```

Build strictly before pushing docs changes:

```bash
pdm run mkdocs build --strict
```

## Structure

```text
docs/
  index.md                    Homepage
  getting-started/            Installation, quickstart, workflows
  concepts/                   Architecture and mental model
  reference/                  CLI, API, config, themes, profiles
  engines/                    WeasyPrint, Playwright, Pandoc
  guides/                     Practical recipes
  advanced/                   Plugins, logging, PDF post-processing
  development/                Testing, release, docs maintenance
  examples/                   Realistic example documents
```

## Style guide

Write docs for three reader levels:

1. A user who only wants to run `markprint README.md README.pdf`.
2. A Python developer integrating Markprint into their own scripts.
3. A package maintainer extending renderers, themes, and profiles.

Avoid placeholders. Every page should answer one of these questions:

- What problem does this solve?
- What command do I run?
- What Python API do I call?
- What can go wrong?
- Where do I customize it?

## RTD

Read the Docs uses `.readthedocs.yaml` and builds `mkdocs.yml`.

If RTD fails, first run:

```bash
pdm run mkdocs build --strict
```

Most failures are caused by nav entries that reference missing files.
