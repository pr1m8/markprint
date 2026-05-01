"""Custom exceptions for Markprint.

Purpose:
    Provide user-friendly exception types for each pipeline boundary.

Examples:
    >>> raise DependencyMissingError("Install optional dependency")
    Traceback (most recent call last):
    ...
    markprint.diagnostics.errors.DependencyMissingError: Install optional dependency
"""


class MarkprintError(Exception):
    """Base exception for Markprint errors."""


class ConfigError(MarkprintError):
    """Raised when configuration cannot be loaded or validated."""


class DependencyMissingError(MarkprintError):
    """Raised when an optional dependency is required but missing."""


class RenderError(MarkprintError):
    """Raised when rendering fails."""


class AssetResolutionError(MarkprintError):
    """Raised when an asset referenced by a document cannot be resolved."""


class ThemeError(MarkprintError):
    """Raised when a theme cannot be loaded."""
