# Quickstart

Install local development dependencies:

```bash
pdm install -G dev -G test -G docs
```

Render a file:

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

Batch render:

```bash
markprint batch docs/*.md --out-dir dist/pdf
```

Compile multiple files into one PDF:

```bash
markprint compile docs/index.md docs/cli.md --output manual.pdf
```
