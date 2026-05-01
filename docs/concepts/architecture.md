# Architecture

```text
SourceLoader -> FrontmatterParser -> MarkdownEngine -> DocumentNormalizer -> HtmlBuilder -> ThemeResolver -> PdfRenderer -> PdfPostProcessor -> OutputWriter
```

The design keeps the command-line experience simple while leaving room for advanced renderers and integrations.
