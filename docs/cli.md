# CLI

The root command accepts positional input and output arguments:

```bash
markprint INPUT [OUTPUT]
```

If `OUTPUT` is omitted, Markprint infers a `.pdf` path from the input path.

## Commands

| Command | Purpose |
| --- | --- |
| `markprint INPUT OUTPUT` | Render one Markdown file or stdin stream |
| `markprint render INPUT OUTPUT` | Explicit render command |
| `markprint render-string TEXT --output PDF` | Render raw Markdown |
| `markprint batch PATTERN --out-dir DIR` | Render many files independently |
| `markprint compile FILES... --output PDF` | Combine files into one PDF |
| `markprint html INPUT --output HTML` | Write debug HTML |
| `markprint themes` | List themes |
| `markprint profiles` | List profiles |
| `markprint engines` | List engines |
| `markprint config` | Show discovered config |
| `markprint doctor` | Check optional dependencies |

## Render options

```bash
markprint report.md report.pdf \
  --profile report \
  --theme nord \
  --toc \
  --page-numbers \
  --code-theme github-dark \
  --debug-html \
  --debug-css
```
