from pathlib import Path

from tokcount.core.counter import count_tokens
from tokcount.core.models import get_model
from tokcount.utils.files import FileEntry


def _make_entry(tmp_path: Path, name: str, content: str) -> FileEntry:
    f = tmp_path / name
    f.write_text(content)
    return FileEntry(path=f.resolve(), size=len(content.encode()), extension=f.suffix)


def test_count_tokens_basic(tmp_path: Path):
    entry = _make_entry(tmp_path, "test.py", "print('hello world')")
    model = get_model("gpt-5")
    result = count_tokens([entry], model)
    assert result.total_tokens > 0
    assert result.total_files == 1
    assert result.context_usage_pct > 0
    assert len(result.errors) == 0


def test_count_tokens_multiple_files(tmp_path: Path):
    entries = [
        _make_entry(tmp_path, "a.py", "x = 1\n"),
        _make_entry(tmp_path, "b.py", "y = 2\n"),
    ]
    model = get_model("gpt-5")
    result = count_tokens(entries, model)
    assert result.total_files == 2
    assert result.total_tokens == sum(f.tokens for f in result.file_counts)


def test_count_tokens_approx_tokenizer(tmp_path: Path):
    content = "a" * 350
    entry = _make_entry(tmp_path, "test.txt", content)
    model = get_model("claude-sonnet-4.5")
    result = count_tokens([entry], model)
    # ~3.5 chars/token -> 350/3.5 = 100
    assert 90 <= result.total_tokens <= 110


def test_cost_calculation(tmp_path: Path):
    content = "x" * 1_000_000  # 1MB of text
    entry = _make_entry(tmp_path, "big.txt", content)
    model = get_model("claude-sonnet-4.5")
    result = count_tokens([entry], model)
    # ~285K tokens at $3/1M = ~$0.86
    assert result.estimated_cost_usd > 0


def test_extension_breakdown(tmp_path: Path):
    entries = [
        _make_entry(tmp_path, "a.py", "x = 1\n" * 10),
        _make_entry(tmp_path, "b.py", "y = 2\n" * 10),
        _make_entry(tmp_path, "c.js", "z = 3\n" * 10),
    ]
    model = get_model("gpt-5")
    result = count_tokens(entries, model)
    exts = {e.extension for e in result.by_extension}
    assert ".py" in exts
    assert ".js" in exts


def test_context_usage_percentage(tmp_path: Path):
    entry = _make_entry(tmp_path, "test.txt", "hello")
    model = get_model("gpt-5")
    result = count_tokens([entry], model)
    assert 0 < result.context_usage_pct < 1  # tiny file in a big context


def test_handles_utf8_errors(tmp_path: Path):
    f = tmp_path / "bad.txt"
    f.write_bytes(b"hello \xff\xfe world")
    entry = FileEntry(path=f.resolve(), size=f.stat().st_size, extension=".txt")
    model = get_model("gpt-5")
    result = count_tokens([entry], model)
    assert result.total_files == 1
    assert len(result.errors) == 0  # errors=replace handles it
