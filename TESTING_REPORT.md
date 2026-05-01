# Testing Report

Command executed:

```bash
pytest tests -q --disable-warnings --import-mode=importlib --cov=markprint --cov-report=term
```

Result:

- 11 passed
- 1 skipped (`python-frontmatter` was not installed in the execution environment)
- Coverage: 75.05%
- Coverage gate: 75%

Notes:

- The scaffold uses lazy imports and safe fallbacks for core HTML rendering so tests can run without optional heavy render dependencies.
- Optional integrations such as WeasyPrint, Playwright, Pandoc, PyMuPDF, pikepdf, and ultilog remain behind extras.
