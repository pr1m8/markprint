"""Simple plugin registry."""

from __future__ import annotations

from typing import Any


class PluginRegistry:
    """Name-to-object registry for extension points."""

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._items: dict[str, Any] = {}

    def register(self, name: str, item: Any) -> None:
        """Register an item.

        Args:
            name: Plugin name.
            item: Plugin object.

        Returns:
            None.
        """
        self._items[name] = item

    def get(self, name: str) -> Any:
        """Get a registered item.

        Args:
            name: Plugin name.

        Returns:
            Registered object.

        Raises:
            KeyError: If missing.
        """
        return self._items[name]

    def names(self) -> list[str]:
        """List plugin names.

        Returns:
            Plugin names.
        """
        return sorted(self._items)
