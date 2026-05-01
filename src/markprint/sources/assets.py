"""Asset resolution helpers for Markprint."""

from __future__ import annotations

from pathlib import Path

from markprint.diagnostics.errors import AssetResolutionError


def resolve_asset(reference: str, *, base_dir: Path) -> Path:
    """Resolve an asset reference against a base directory.

    Args:
        reference: Relative or absolute asset reference.
        base_dir: Base directory for relative references.

    Returns:
        Resolved asset path.

    Raises:
        AssetResolutionError: If the asset does not exist.

    Examples:
        >>> resolve_asset("missing.png", base_dir=Path("."))  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ...
        AssetResolutionError: ...
    """
    path = Path(reference)
    resolved = path if path.is_absolute() else base_dir / path
    if not resolved.exists():
        raise AssetResolutionError(f"Could not resolve asset {reference!r} from {base_dir}")
    return resolved
