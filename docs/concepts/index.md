# Concepts

Markprint is easiest to understand as a small compiler for Markdown documents. It separates input loading, Markdown parsing, HTML building, theme resolution, PDF rendering, and post-processing.

| Object | Purpose |
|---|---|
| `MarkdownSource` | Normalized source input |
| `ParsedDocument` | Markdown body plus metadata |
| `HtmlDocument` | Rendered HTML body plus headings |
| `StyledHtmlDocument` | Full printable HTML and CSS |
| `PdfArtifact` | PDF bytes, output path, and metadata |
| `RenderOptions` | Validated user-facing render options |
