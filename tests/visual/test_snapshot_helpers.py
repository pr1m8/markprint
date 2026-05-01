"""Visual testing helper smoke tests."""

from __future__ import annotations

from markprint.testing.snapshots import snapshot_name


def test_snapshot_name_normalizes_spaces() -> None:
    """Snapshot names should be filesystem-friendly."""
    assert snapshot_name("GitHub Theme") == "github-theme"
