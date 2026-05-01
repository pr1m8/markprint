"""Diagnostic report utilities for Markprint.

Purpose:
    Build human-readable render summaries and troubleshooting messages.

Design:
    Diagnostic helpers return strings or Rich renderables but do not perform
    rendering themselves. This keeps diagnostics reusable from the CLI, tests,
    and library callers.

Examples:
    >>> summarize_render(source='README.md', output='README.pdf', engine='weasyprint')
    'README.md -> README.pdf using weasyprint'
"""

from __future__ import annotations


def summarize_render(*, source: str, output: str, engine: str) -> str:
    """Return a concise render summary.

    Args:
        source: Source description.
        output: Output description.
        engine: PDF engine name.

    Returns:
        Render summary string.

    Raises:
        None.

    Examples:
        >>> summarize_render(source='a.md', output='a.pdf', engine='weasyprint')
        'a.md -> a.pdf using weasyprint'
    """
    return f"{source} -> {output} using {engine}"


def missing_dependency_message(extra: str, package: str) -> str:
    """Return a friendly optional dependency installation message.

    Args:
        extra: Markprint extra name.
        package: Missing package or feature name.

    Returns:
        Installation hint.

    Raises:
        None.

    Examples:
        >>> missing_dependency_message('browser', 'Playwright')
        "Playwright requires: pip install 'markprint[browser]'"
    """
    return f"{package} requires: pip install 'markprint[{extra}]'"
