from pathlib import Path

from typer.testing import CliRunner

from tokcount.cli import app

runner = CliRunner()


def test_count_help():
    result = runner.invoke(app, ["count", "--help"])
    assert result.exit_code == 0
    assert "Count tokens" in result.stdout


def test_models_list():
    result = runner.invoke(app, ["models"])
    assert result.exit_code == 0
    assert "gpt-5" in result.stdout
    assert "Anthropic" in result.stdout
    assert "OpenAI" in result.stdout


def test_models_detail():
    result = runner.invoke(app, ["models", "gpt-5"])
    assert result.exit_code == 0
    assert "OpenAI" in result.stdout
    assert "256,000" in result.stdout


def test_models_unknown():
    result = runner.invoke(app, ["models", "nope"])
    assert result.exit_code == 1


def test_count_single_file(tmp_path: Path):
    f = tmp_path / "test.py"
    f.write_text("print('hello')")
    result = runner.invoke(app, ["count", str(f)])
    assert result.exit_code == 0
    assert "Token Count" in result.stdout


def test_count_directory(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    result = runner.invoke(app, ["count", str(tmp_path)])
    assert result.exit_code == 0


def test_count_with_model(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    result = runner.invoke(app, ["count", str(tmp_path), "-m", "gpt-5"])
    assert result.exit_code == 0
    assert "gpt-5" in result.stdout


def test_count_multi_model(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    result = runner.invoke(app, ["count", str(tmp_path), "-m", "gpt-5", "-m", "haiku"])
    assert result.exit_code == 0
    assert "gpt-5" in result.stdout
    assert "claude-haiku-4.5" in result.stdout


def test_count_json_format(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    result = runner.invoke(app, ["count", str(tmp_path), "-f", "json"])
    assert result.exit_code == 0
    assert '"total_tokens"' in result.stdout


def test_count_nonexistent_path():
    result = runner.invoke(app, ["count", "/nonexistent/path"])
    assert result.exit_code != 0


def test_count_unknown_model(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    result = runner.invoke(app, ["count", str(tmp_path), "-m", "fake"])
    assert result.exit_code != 0


def test_count_empty_directory(tmp_path: Path):
    result = runner.invoke(app, ["count", str(tmp_path)])
    assert result.exit_code == 1
