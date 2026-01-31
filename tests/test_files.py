from pathlib import Path

from tokcount.utils.files import discover_files


def test_discover_single_file(tmp_path: Path):
    f = tmp_path / "hello.py"
    f.write_text("print('hello')")
    files = discover_files([f])
    assert len(files) == 1
    assert files[0].extension == ".py"


def test_discover_directory(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    (tmp_path / "b.txt").write_text("hello")
    files = discover_files([tmp_path])
    assert len(files) == 2


def test_ignores_binary_extensions(tmp_path: Path):
    (tmp_path / "image.png").write_bytes(b"\x89PNG")
    (tmp_path / "code.py").write_text("x = 1")
    files = discover_files([tmp_path])
    assert len(files) == 1
    assert files[0].extension == ".py"


def test_ignores_default_dirs(tmp_path: Path):
    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()
    (node_modules / "pkg.js").write_text("module.exports = {}")
    (tmp_path / "app.js").write_text("console.log('hi')")
    files = discover_files([tmp_path])
    assert len(files) == 1


def test_ignores_lock_files(tmp_path: Path):
    (tmp_path / "package-lock.json").write_text("{}")
    (tmp_path / "package.json").write_text("{}")
    files = discover_files([tmp_path])
    assert len(files) == 1
    assert files[0].path.name == "package.json"


def test_include_filter(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    (tmp_path / "b.js").write_text("x = 1")
    files = discover_files([tmp_path], include=["*.py"])
    assert len(files) == 1
    assert files[0].extension == ".py"


def test_exclude_filter(tmp_path: Path):
    (tmp_path / "a.py").write_text("x = 1")
    (tmp_path / "b.js").write_text("x = 1")
    files = discover_files([tmp_path], exclude=["*.js"])
    assert len(files) == 1
    assert files[0].extension == ".py"


def test_skips_empty_files(tmp_path: Path):
    (tmp_path / "empty.py").write_text("")
    (tmp_path / "notempty.py").write_text("x = 1")
    files = discover_files([tmp_path])
    assert len(files) == 1


def test_recursive_discovery(tmp_path: Path):
    sub = tmp_path / "sub"
    sub.mkdir()
    (tmp_path / "a.py").write_text("x = 1")
    (sub / "b.py").write_text("y = 2")
    files = discover_files([tmp_path])
    assert len(files) == 2
