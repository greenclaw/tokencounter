import json
from pathlib import Path

from tokcount.core.counter import CountResult


def render_json(results: list[CountResult], top_n: int, base_path: Path | None = None) -> str:
    """Render token count results as JSON."""
    base = base_path or Path.cwd()
    output = [_serialize_result(r, top_n, base) for r in results]

    if len(output) == 1:
        return json.dumps(output[0], indent=2)
    return json.dumps(output, indent=2)


def _relative_path(path: Path, base: Path) -> str:
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def _serialize_result(result: CountResult, top_n: int, base: Path) -> dict:
    model = result.model
    sorted_files = sorted(result.file_counts, key=lambda f: f.tokens, reverse=True)[:top_n]

    return {
        "model": {
            "name": model.name,
            "provider": model.provider,
            "context_window": model.context_window,
            "input_price_per_mtok": model.input_price_per_mtok,
        },
        "summary": {
            "total_tokens": result.total_tokens,
            "total_files": result.total_files,
            "total_bytes": result.total_size,
            "context_usage_pct": round(result.context_usage_pct, 2),
            "estimated_cost_usd": round(result.estimated_cost_usd, 6),
            "tokenizer": result.tokenizer_name,
            "is_exact": result.is_exact,
        },
        "top_files": [
            {
                "path": _relative_path(fc.path, base),
                "tokens": fc.tokens,
                "bytes": fc.size,
            }
            for fc in sorted_files
        ],
        "by_extension": [
            {
                "extension": eb.extension,
                "files": eb.files,
                "tokens": eb.tokens,
                "percentage": round(eb.percentage, 2),
            }
            for eb in result.by_extension
        ],
        "errors": result.errors,
    }
