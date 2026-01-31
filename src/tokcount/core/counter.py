from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from tokcount.core.models import ModelInfo
from tokcount.core.tokenizers import get_tokenizer
from tokcount.utils.files import FileEntry


@dataclass
class FileTokenCount:
    path: Path
    tokens: int
    size: int
    extension: str


@dataclass
class ExtensionBreakdown:
    extension: str
    files: int
    tokens: int
    percentage: float


@dataclass
class CountResult:
    model: ModelInfo
    total_tokens: int
    total_files: int
    total_size: int
    file_counts: list[FileTokenCount]
    by_extension: list[ExtensionBreakdown]
    context_usage_pct: float
    estimated_cost_usd: float
    errors: list[str] = field(default_factory=list)
    tokenizer_name: str = ""
    is_exact: bool = True


def count_tokens(files: list[FileEntry], model: ModelInfo) -> CountResult:
    """Count tokens for all files using the model's tokenizer."""
    tokenizer = get_tokenizer(model.tokenizer)
    file_counts: list[FileTokenCount] = []
    errors: list[str] = []

    for entry in files:
        try:
            text = entry.path.read_text(encoding="utf-8", errors="replace")
            tokens = tokenizer.count(text)
            file_counts.append(FileTokenCount(
                path=entry.path,
                tokens=tokens,
                size=entry.size,
                extension=entry.extension,
            ))
        except OSError as e:
            errors.append(f"{entry.path}: {e}")

    total_tokens = sum(f.tokens for f in file_counts)
    total_size = sum(f.size for f in file_counts)

    # Extension breakdown
    ext_tokens: dict[str, int] = defaultdict(int)
    ext_files: dict[str, int] = defaultdict(int)
    for fc in file_counts:
        ext = fc.extension or "(no ext)"
        ext_tokens[ext] += fc.tokens
        ext_files[ext] += fc.files if hasattr(fc, "files") else 1

    by_extension = [
        ExtensionBreakdown(
            extension=ext,
            files=ext_files[ext],
            tokens=ext_tokens[ext],
            percentage=(ext_tokens[ext] / total_tokens * 100) if total_tokens > 0 else 0,
        )
        for ext in sorted(ext_tokens, key=ext_tokens.get, reverse=True)
    ]

    context_pct = (total_tokens / model.context_window * 100) if model.context_window > 0 else 0
    cost = total_tokens / 1_000_000 * model.input_price_per_mtok

    return CountResult(
        model=model,
        total_tokens=total_tokens,
        total_files=len(file_counts),
        total_size=total_size,
        file_counts=file_counts,
        by_extension=by_extension,
        context_usage_pct=context_pct,
        estimated_cost_usd=cost,
        errors=errors,
        tokenizer_name=tokenizer.name,
        is_exact=tokenizer.is_exact,
    )
