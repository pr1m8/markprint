"""Entry point discovery helpers."""

from __future__ import annotations

from importlib.metadata import entry_points
from typing import Any


def load_entrypoint_group(group: str) -> dict[str, Any]:
    """Load entry points for a group.

    Args:
        group: Entry point group name.

    Returns:
        Mapping of entry point names to loaded objects.
    """
    return {ep.name: ep.load() for ep in entry_points(group=group)}
