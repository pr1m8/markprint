# Design

Markprint is a staged Markdown document compiler.

## Goals

- Keep the common path simple: `markprint README.md README.pdf`.
- Keep the internals deeply modular.
- Support files, raw Markdown strings, stdin, batch rendering, and multi-file compilation.
- Make WeasyPrint the default static PDF backend.
- Add Playwright and Pandoc as optional power backends.
- Keep logging optional with a standard backend and an `ultilog` backend.

## Pipeline

```text
MarkdownSource
  -> ParsedDocument
  -> HtmlDocument
  -> StyledHtmlDocument
  -> PdfArtifact
```

## Stage responsibilities

| Stage | Responsibility |
| --- | --- |
| Source loader | File, stdin, raw string, multi-file compile |
| Frontmatter parser | Extract metadata and body |
| Markdown engine | Render body Markdown to HTML |
| HTML builder | Wrap body in template and CSS |
| Theme registry | Resolve built-in or path-based themes |
| PDF renderer | Convert styled HTML to PDF bytes |
| Post-processor | Metadata, merge, preview, optimization |
| Logging adapter | Optional logs and render events |

## Extension points

- Markdown engines
- PDF renderers
- Themes
- Profiles
- Diagram renderers
- Math renderers
- Logging backends
- PDF post-processors

## Config precedence

1. CLI flags
2. Python API explicit options
3. Markdown frontmatter
4. Project config
5. Built-in defaults

## Optional dependency principle

The default install should be useful and beautiful. Browser automation, Pandoc, LaTeX, PDF manipulation, and advanced observability should remain optional.
