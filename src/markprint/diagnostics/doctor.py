"""Environment doctor checks for Markprint.

Purpose:
    Provide programmatic checks for core and optional dependencies.

Examples:
    >>> result = check_module('sys')
    >>> result.available
    True
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DoctorCheck:
    """Result of one doctor check.

    Args:
        name: Check name.
        available: Whether the module or feature is available.
        hint: Optional installation hint.

    Returns:
        A doctor check instance.
    """

    name: str
    available: bool
    hint: str = ""


def check_module(module_name: str, *, hint: str = "") -> DoctorCheck:
    """Check whether a module can be imported.

    Args:
        module_name: Python module name.
        hint: Optional installation hint.

    Returns:
        Doctor check result.

    Raises:
        None.

    Examples:
        >>> check_module('sys').available
        True
    """
    try:
        __import__(module_name)
    except ImportError:
        return DoctorCheck(module_name, False, hint)
    return DoctorCheck(module_name, True, hint)


def run_default_checks() -> list[DoctorCheck]:
    """Run default dependency checks.

    Args:
        None.

    Returns:
        Doctor check results.

    Raises:
        None.
    """
    return [
        check_module("markdown_it"),
        check_module("jinja2"),
        check_module("pygments"),
        check_module("weasyprint", hint="pip install weasyprint"),
        check_module("playwright", hint="pip install 'markprint[browser]'"),
        check_module("pypandoc", hint="pip install 'markprint[pandoc]'"),
        check_module("ultilog", hint="pip install 'markprint[logging]'"),
    ]
