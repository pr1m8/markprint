"""Pytest fixtures for Markprint tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def sample_markdown() -> str:
    """Return sample Markdown text."""
    return "# Hello\n\nThis is **Markprint**."


@pytest.fixture
def sample_file(tmp_path: Path, sample_markdown: str) -> Path:
    """Create a sample Markdown file."""
    path = tmp_path / "sample.md"
    path.write_text(sample_markdown, encoding="utf-8")
    return path
