# Testing

```bash
pdm install -G test
pdm run pytest --cov=markprint --cov-report=term-missing
pdm run ruff check .
pdm run ruff format --check .
```
