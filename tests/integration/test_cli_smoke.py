"""CLI smoke tests."""

from __future__ import annotations

from typer.testing import CliRunner

from markprint.cli import app


def test_themes_command_lists_default_theme() -> None:
    """The themes command should list bundled themes."""
    result = CliRunner().invoke(app, ["themes"])

    assert result.exit_code == 0
    assert "default" in result.output


def test_profiles_command_lists_report_profile() -> None:
    """The profiles command should list built-in profiles."""
    result = CliRunner().invoke(app, ["profiles"])

    assert result.exit_code == 0
    assert "report" in result.output
