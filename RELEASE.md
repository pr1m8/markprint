# Release Guide

Markprint publishes to PyPI through GitHub Actions and PyPI Trusted Publishing.

## PyPI Trusted Publisher settings

Configure these values on PyPI:

```text
Owner: pr1m8
Repository: markprint
Workflow filename: release.yml
Environment name: pypi
```

## Pre-release checklist

Run from the repository root:

```bash
pdm install -G dev -G test -G docs
pdm run ruff check .
pdm run ruff format --check .
pdm run pytest --cov=markprint --cov-report=term-missing
pdm run mkdocs build --strict
rm -rf dist build *.egg-info src/*.egg-info
pdm run python -m build
pdm run twine check dist/*
```

## Bump version

```bash
python - <<'PY_VERSION'
from pathlib import Path
import re

path = Path("pyproject.toml")
text = path.read_text()
old = re.search(r'^version = "([^"]+)"', text, flags=re.MULTILINE).group(1)
major, minor, patch = map(int, old.split("."))
new = f"{major}.{minor}.{patch + 1}"
text = re.sub(r'^version = "[^"]+"', f'version = "{new}"', text, count=1, flags=re.MULTILINE)
path.write_text(text)
print(f"{old} -> {new}")
PY_VERSION
```

## Commit and publish

```bash
git add pyproject.toml
git commit -m "chore(release): bump version"
git push origin main

VERSION="$(python - <<'PY_VERSION'
from pathlib import Path
import re
text = Path("pyproject.toml").read_text()
print(re.search(r'^version = "([^"]+)"', text, flags=re.MULTILINE).group(1))
PY_VERSION
)"

git tag "v$VERSION"
git push origin "v$VERSION"

gh release create "v$VERSION"   --title "v$VERSION"   --notes "Release v$VERSION."
```

## Watch release

```bash
gh run watch
gh run list --workflow release.yml --limit 5
python -m pip index versions markprint
```

## Troubleshooting

If PyPI does not update, inspect the release workflow:

```bash
gh run view --log-failed
```

Common causes:

- the release workflow failed before the publish step,
- PyPI Trusted Publisher settings do not match,
- the version already exists on PyPI,
- the package failed `twine check`,
- the workflow is running on an older tag before the fixed workflow was committed.
