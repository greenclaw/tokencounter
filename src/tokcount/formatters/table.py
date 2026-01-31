from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from tokcount.core.counter import CountResult


def _format_tokens(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def _format_bytes(n: int) -> str:
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f} MB"
    if n >= 1_000:
        return f"{n / 1_000:.1f} KB"
    return f"{n} B"


def _context_color(pct: float) -> str:
    if pct <= 50:
        return "green"
    if pct <= 80:
        return "yellow"
    return "red"


def _relative_path(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def render_table(results: list[CountResult], top_n: int, base_path: Path | None = None) -> None:
    """Render token count results as Rich tables."""
    console = Console()
    base = base_path or Path.cwd()

    for result in results:
        _render_single(console, result, top_n, base)
        if result is not results[-1]:
            console.print()


def _render_single(console: Console, result: CountResult, top_n: int, base: Path) -> None:
    model = result.model
    color = _context_color(result.context_usage_pct)
    approx = " (approx)" if not result.is_exact else ""

    # Summary panel
    summary_lines = [
        f"[bold]{model.name}[/bold] ({model.provider})",
        f"Tokens: [bold]{_format_tokens(result.total_tokens)}[/bold]{approx}  |  "
        f"Files: {result.total_files}  |  "
        f"Size: {_format_bytes(result.total_size)}",
        f"Context: [{color}]{result.context_usage_pct:.1f}%[/{color}] of "
        f"{_format_tokens(model.context_window)}  |  "
        f"Cost: ${result.estimated_cost_usd:.4f}",
    ]
    if not result.is_exact:
        summary_lines.append(f"[dim]Tokenizer: {result.tokenizer_name}[/dim]")

    console.print(Panel("\n".join(summary_lines), title="Token Count", border_style=color))

    # Top files table
    sorted_files = sorted(result.file_counts, key=lambda f: f.tokens, reverse=True)[:top_n]
    if sorted_files:
        table = Table(title=f"Top {min(top_n, len(sorted_files))} Files by Token Count")
        table.add_column("File", style="cyan", no_wrap=True, max_width=60)
        table.add_column("Tokens", justify="right", style="bold")
        table.add_column("% of Total", justify="right")
        table.add_column("Size", justify="right", style="dim")

        for fc in sorted_files:
            pct = (fc.tokens / result.total_tokens * 100) if result.total_tokens > 0 else 0
            bar = _mini_bar(pct)
            table.add_row(
                _relative_path(fc.path, base),
                _format_tokens(fc.tokens),
                f"{bar} {pct:.1f}%",
                _format_bytes(fc.size),
            )
        console.print(table)

    # Extension breakdown
    if result.by_extension:
        ext_table = Table(title="By Extension")
        ext_table.add_column("Ext", style="cyan")
        ext_table.add_column("Files", justify="right")
        ext_table.add_column("Tokens", justify="right", style="bold")
        ext_table.add_column("% of Total", justify="right")

        for eb in result.by_extension[:10]:
            ext_table.add_row(
                eb.extension or "(none)",
                str(eb.files),
                _format_tokens(eb.tokens),
                f"{eb.percentage:.1f}%",
            )
        console.print(ext_table)

    # Errors
    if result.errors:
        error_text = Text()
        for err in result.errors:
            error_text.append(f"  {err}\n", style="red")
        console.print(Panel(error_text, title="Errors", border_style="red"))


def _mini_bar(pct: float, width: int = 10) -> str:
    filled = round(pct / 100 * width)
    return "\u2588" * filled + "\u2591" * (width - filled)
