.PHONY: install test lint typecheck docs build clean

install:
	pdm install -G dev -G test -G docs

test:
	pdm run pytest --cov=markprint --cov-report=term-missing

lint:
	pdm run ruff check .
	pdm run ruff format --check .

typecheck:
	pdm run pyright

docs:
	pdm run mkdocs build

build:
	pdm run python -m build
	pdm run twine check dist/*

clean:
	rm -rf dist build *.egg-info htmlcov .coverage .pytest_cache .ruff_cache site
