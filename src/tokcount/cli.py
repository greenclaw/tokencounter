from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console
from rich.table import Table

from tokcount.core.counter import count_tokens
from tokcount.core.models import ModelInfo, get_default_model, get_model, list_models
from tokcount.formatters.json_fmt import render_json
from tokcount.formatters.table import render_table
from tokcount.utils.files import discover_files

app = typer.Typer(
    name="tokcount",
    help="Count tokens in files and directories for different LLM models.",
    no_args_is_help=True,
)


def _resolve_models(model_names: list[str] | None) -> list[ModelInfo]:
    if not model_names:
        return [get_default_model()]
    models = []
    for name in model_names:
        try:
            models.append(get_model(name))
        except KeyError:
            msg = f"Unknown model: {name!r}. Run 'tokcount models' to list."
            raise typer.BadParameter(msg)
    return models


@app.command()
def count(
    paths: Annotated[
        list[Path], typer.Argument(help="Files or directories to scan.")
    ],
    model: Annotated[
        Optional[list[str]],
        typer.Option("--model", "-m", help="Model(s) to use. Repeatable."),
    ] = None,
    format: Annotated[
        str, typer.Option("--format", "-f", help="Output format: table or json.")
    ] = "table",
    top: Annotated[
        int, typer.Option("--top", "-t", help="Number of top files to show.")
    ] = 10,
    include: Annotated[
        Optional[list[str]],
        typer.Option("--include", help="Include only matching globs."),
    ] = None,
    exclude: Annotated[
        Optional[list[str]],
        typer.Option("--exclude", help="Exclude matching globs."),
    ] = None,
) -> None:
    """Count tokens in files and directories."""
    # Validate paths exist
    for p in paths:
        if not p.exists():
            raise typer.BadParameter(f"Path does not exist: {p}")

    models = _resolve_models(model)
    files = discover_files(paths, include=include, exclude=exclude)

    if not files:
        typer.echo("No files found.")
        raise typer.Exit(1)

    results = [count_tokens(files, m) for m in models]

    base_path = paths[0].resolve() if paths[0].is_dir() else paths[0].parent.resolve()

    if format == "json":
        typer.echo(render_json(results, top_n=top, base_path=base_path))
    elif format == "table":
        render_table(results, top_n=top, base_path=base_path)
    else:
        raise typer.BadParameter(f"Unknown format: {format!r}. Use 'table' or 'json'.")


@app.command()
def models(
    name: Annotated[Optional[str], typer.Argument(help="Show detail for a specific model.")] = None,
) -> None:
    """List available models or show detail for one."""
    console = Console()

    if name:
        try:
            m = get_model(name)
        except KeyError:
            typer.echo(f"Unknown model: {name!r}")
            raise typer.Exit(1)
        _show_model_detail(console, m)
        return

    table = Table(title="Supported Models")
    table.add_column("Model", style="cyan")
    table.add_column("Provider")
    table.add_column("Context", justify="right")
    table.add_column("Input $/1M tok", justify="right")
    table.add_column("Tokenizer")
    table.add_column("Aliases", style="dim")

    for m in list_models():
        ctx = f"{m.context_window:,}"
        table.add_row(
            m.name,
            m.provider,
            ctx,
            f"${m.input_price_per_mtok:.2f}",
            m.tokenizer,
            ", ".join(m.aliases) if m.aliases else "",
        )
    console.print(table)


def _show_model_detail(console: Console, m: ModelInfo) -> None:
    from rich.panel import Panel

    lines = [
        f"[bold]{m.name}[/bold]",
        f"Provider: {m.provider}",
        f"Context window: {m.context_window:,} tokens",
        f"Input price: ${m.input_price_per_mtok:.2f} / 1M tokens",
        f"Output price: ${m.output_price_per_mtok:.2f} / 1M tokens",
        f"Tokenizer: {m.tokenizer}",
    ]
    if m.aliases:
        lines.append(f"Aliases: {', '.join(m.aliases)}")
    console.print(Panel("\n".join(lines), title="Model Detail"))
