"""Theme registry and loader."""
from __future__ import annotations
from importlib.resources import files
from pathlib import Path
from markprint.diagnostics.errors import ThemeError
from markprint.themes.models import ThemeSpec
BUILTIN_THEMES = ["default", "github", "nord", "dracula", "report", "resume", "academic"]
class ThemeRegistry:
    """Resolve built-in and path-based themes."""
    def list_builtin(self) -> list[str]:
        """List built-in theme names.

        Args:
            None.

        Returns:
            Theme names.

        Raises:
            None.
        """
        return list(BUILTIN_THEMES)
    def load(self, name_or_path: str) -> ThemeSpec:
        """Load a theme by built-in name or filesystem path.

        Args:
            name_or_path: Built-in theme name or directory path.

        Returns:
            Loaded theme spec.

        Raises:
            ThemeError: If the theme cannot be found.
        """
        path = Path(name_or_path)
        if path.exists():
            return self._load_from_path(path, path.name)
        if name_or_path not in BUILTIN_THEMES:
            raise ThemeError(f"Unknown theme {name_or_path!r}. Available: {', '.join(BUILTIN_THEMES)}")
        base = files("markprint.themes.builtin") / name_or_path
        css = ""
        for filename in ["variables.css", "theme.css"]:
            resource = base / filename
            if resource.is_file():
                css += resource.read_text(encoding="utf-8") + "\n"
        return ThemeSpec(name=name_or_path, css=css)
    def _load_from_path(self, path: Path, name: str) -> ThemeSpec:
        css = ""
        for filename in ["variables.css", "theme.css"]:
            candidate = path / filename
            if candidate.exists():
                css += candidate.read_text(encoding="utf-8") + "\n"
        if not css:
            raise ThemeError(f"Theme path {path} does not contain theme.css or variables.css")
        return ThemeSpec(name=name, css=css, base_dir=path)
