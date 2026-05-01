"""Unit tests for theme registry."""
from markprint.themes.registry import ThemeRegistry

def test_builtin_themes() -> None:
    registry = ThemeRegistry()
    assert "default" in registry.list_builtin()
    assert registry.load("default").css
