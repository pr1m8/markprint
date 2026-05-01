"""Command-line entry point for ``python -m markprint``.

Purpose:
    Forward module execution to the Typer application.

Examples:
    .. code-block:: bash

        python -m markprint README.md README.pdf
"""

from markprint.cli import app

if __name__ == "__main__":
    app()
