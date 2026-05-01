"""Typer command-line interface for Markprint.

Purpose:
    Provide an ergonomic CLI for file, raw string, stdin, batch, and compiled
    Markdown-to-PDF rendering.

Design:
    The root command accepts ``INPUT`` and ``OUTPUT`` positionally for the
    common path while subcommands expose richer workflows.

Examples:
    .. code-block:: bash

        markprint README.md README.pdf
        echo "# Hello" | markprint - hello.pdf
        markprint render-string "# Hello" --output hello.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from markprint.api import render_html, render_pdf
from markprint.config import discover_config, list_profiles
from markprint.config.models import LoggingSettings, RenderOptions
from markprint.diagnostics.errors import MarkprintError
from markprint.sources.globbing import expand_inputs
from markprint.sources.models import MarkdownSource
from markprint.sources.resolver import infer_output_path
from markprint.themes.registry import ThemeRegistry

app = typer.Typer(help="Beautiful Markdown-to-PDF rendering.", no_args_is_help=False)
console = Console()


def _options(
    *,
    theme: str,
    profile: str,
    engine: str,
    markdown_engine: str,
    toc: bool,
    page_numbers: bool,
    code_theme: str,
    page_size: str,
    margin: str,
    output: Path | None = None,
    out_dir: Path | None = None,
    debug_html: bool = False,
    debug_css: bool = False,
    logging_enabled: bool = False,
    logging_backend: str = "stdlib",
    log_level: str = "INFO",
) -> RenderOptions:
    """Build render options from CLI values.

    Args:
        theme: Theme name.
        profile: Profile name.
        engine: PDF engine name.
        markdown_engine: Markdown engine name.
        toc: Whether to generate a table of contents.
        page_numbers: Whether to render page numbers.
        code_theme: Pygments code theme.
        page_size: CSS page size.
        margin: CSS page margin.
        output: Optional output path.
        out_dir: Optional batch output directory.
        debug_html: Whether to write debug HTML.
        debug_css: Whether to write debug CSS.
        logging_enabled: Whether to configure logging.
        logging_backend: Logging backend name.
        log_level: Logging level.

    Returns:
        Validated render options.

    Raises:
        pydantic.ValidationError: If values are invalid.
    """
    return RenderOptions(
        output=output,
        out_dir=out_dir,
        theme=theme,
        profile=profile,
        engine=engine,  # type: ignore[arg-type]
        markdown_engine=markdown_engine,  # type: ignore[arg-type]
        toc=toc,
        page_numbers=page_numbers,
        code_theme=code_theme,
        page_size=page_size,
        margin=margin,
        debug_html=debug_html,
        debug_css=debug_css,
        logging=LoggingSettings(
            enabled=logging_enabled,
            backend=logging_backend,  # type: ignore[arg-type]
            level=log_level,
        ),
    )


def _print_success(output: Path | None) -> None:
    """Print a consistent success message.

    Args:
        output: Output path.

    Returns:
        None.
    """
    console.print(f"[bold green]✓[/] Wrote {output or 'PDF bytes'}")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Show help when no subcommand is supplied.

    Args:
        ctx: Typer context.

    Returns:
        None.

    Raises:
        typer.Exit: To display help for empty invocations.
    """
    if ctx.invoked_subcommand is None:
        console.print(ctx.get_help())
        raise typer.Exit(0)


@app.command("render")
def render_command(
    input: Annotated[Path, typer.Argument(help="Input Markdown path or '-' for stdin.")],
    output: Annotated[Path | None, typer.Argument(help="Output PDF path.")] = None,
    theme: Annotated[str, typer.Option(help="Theme name or path.")] = "default",
    profile: Annotated[str, typer.Option(help="Document profile.")] = "docs",
    engine: Annotated[str, typer.Option(help="PDF engine.")] = "weasyprint",
    markdown_engine: Annotated[str, typer.Option(help="Markdown engine.")] = "markdown-it",
    toc: Annotated[bool, typer.Option("--toc/--no-toc")] = False,
    page_numbers: Annotated[bool, typer.Option("--page-numbers/--no-page-numbers")] = True,
    code_theme: Annotated[str, typer.Option(help="Pygments code theme.")] = "default",
    page_size: Annotated[str, typer.Option(help="CSS page size.")] = "Letter",
    margin: Annotated[str, typer.Option(help="CSS page margin.")] = "0.8in",
    debug_html: Annotated[bool, typer.Option("--debug-html/--no-debug-html")] = False,
    debug_css: Annotated[bool, typer.Option("--debug-css/--no-debug-css")] = False,
    logging_enabled: Annotated[bool, typer.Option("--logging/--no-logging")] = False,
    logging_backend: Annotated[str, typer.Option(help="Logging backend.")] = "stdlib",
    log_level: Annotated[str, typer.Option(help="Logging level.")] = "INFO",
) -> None:
    """Render one Markdown source to PDF."""
    try:
        if str(input) == "-":
            source = MarkdownSource.from_stdin(sys.stdin.read())
            final_output = output or Path("stdin.pdf")
        else:
            source = MarkdownSource.from_file(input)
            final_output = output or infer_output_path(input)
        options = _options(
            theme=theme,
            profile=profile,
            engine=engine,
            markdown_engine=markdown_engine,
            toc=toc,
            page_numbers=page_numbers,
            code_theme=code_theme,
            page_size=page_size,
            margin=margin,
            output=final_output,
            debug_html=debug_html,
            debug_css=debug_css,
            logging_enabled=logging_enabled,
            logging_backend=logging_backend,
            log_level=log_level,
        )
        artifact = render_pdf(source=source, options=options)
        _print_success(artifact.output_path or final_output)
    except (MarkprintError, Exception) as exc:
        console.print(Panel(str(exc), title="[bold red]Render failed[/]", border_style="red"))
        raise typer.Exit(1) from exc


@app.command("render-string")
def render_string(
    markdown: Annotated[str, typer.Argument(help="Raw Markdown text.")],
    output: Annotated[Path, typer.Option("--output", "-o")],
    theme: str = "default",
    engine: str = "weasyprint",
    base_url: Annotated[Path | None, typer.Option(help="Base directory for relative assets.")] = None,
) -> None:
    """Render a raw Markdown string to PDF."""
    options = RenderOptions(output=output, theme=theme, engine=engine)  # type: ignore[arg-type]
    artifact = render_pdf(markdown=markdown, output=output, options=options, base_url=base_url)
    _print_success(artifact.output_path or output)


@app.command("batch")
def batch(
    inputs: list[str],
    out_dir: Annotated[Path, typer.Option("--out-dir", "-d")],
    theme: str = "default",
    profile: str = "docs",
) -> None:
    """Render multiple Markdown files into separate PDFs."""
    for path in expand_inputs(inputs):
        output = infer_output_path(path, out_dir=out_dir)
        render_pdf(path, output=output, options=RenderOptions(output=output, theme=theme, profile=profile))
        console.print(f"[green]✓[/] {path} -> {output}")


@app.command("compile")
def compile_command(
    inputs: list[Path],
    output: Annotated[Path, typer.Option("--output", "-o")],
    theme: str = "default",
    profile: str = "book",
) -> None:
    """Compile multiple Markdown files into one PDF."""
    source = MarkdownSource.compile_files(inputs)
    artifact = render_pdf(source=source, output=output, options=RenderOptions(output=output, theme=theme, profile=profile))
    _print_success(artifact.output_path or output)


@app.command("html")
def html_command(input: Path, output: Annotated[Path, typer.Option("--output", "-o")], theme: str = "default") -> None:
    """Render Markdown to debug HTML."""
    styled = render_html(input, options=RenderOptions(theme=theme))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(styled.html, encoding="utf-8")
    _print_success(output)


@app.command("themes")
def themes() -> None:
    """List built-in themes."""
    for name in ThemeRegistry().list_builtin():
        typer.echo(name)


@app.command("profiles")
def profiles() -> None:
    """List built-in document profiles."""
    for name in list_profiles():
        typer.echo(name)


@app.command("engines")
def engines() -> None:
    """List available engine names."""
    table = Table(title="Engines")
    table.add_column("Type")
    table.add_column("Names")
    table.add_row("Markdown", "markdown-it, python-markdown, pandoc")
    table.add_row("PDF", "weasyprint, playwright, pandoc")
    console.print(table)


@app.command("config")
def config_command() -> None:
    """Show discovered project configuration."""
    config = discover_config(Path.cwd())
    console.print(Panel(repr(config) if config else "No project config found.", title="markprint config"))


@app.command("doctor")
def doctor() -> None:
    """Inspect optional dependency availability."""
    table = Table(title="Markprint Doctor")
    table.add_column("Check")
    table.add_column("Status")
    checks = ["markdown_it", "jinja2", "pygments", "weasyprint", "playwright", "pypandoc", "ultilog"]
    for module in checks:
        try:
            __import__(module)
            status = "[green]available[/]"
        except ImportError:
            status = "[yellow]missing[/]"
        table.add_row(module, status)
    console.print(table)
