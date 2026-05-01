"""Unit tests for render options."""

from pathlib import Path

from markprint.config.models import RenderOptions


def test_default_options() -> None:
    options = RenderOptions()
    assert options.engine == "weasyprint"
    assert options.theme == "default"


def test_output_inference() -> None:
    assert RenderOptions().with_output_default(Path("README.md")).output == Path("README.pdf")
