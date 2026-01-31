import fnmatch
from dataclasses import dataclass
from pathlib import Path

DEFAULT_IGNORE_DIRS = frozenset({
    ".git", ".hg", ".svn",
    "node_modules", "bower_components",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    ".tox", ".nox", ".venv", "venv", "env",
    ".next", ".nuxt", "dist", "build", "target",
    ".idea", ".vscode",
    ".terraform",
})

BINARY_EXTENSIONS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".webp", ".svg",
    ".mp3", ".mp4", ".wav", ".avi", ".mov", ".mkv",
    ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z", ".rar",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".exe", ".dll", ".so", ".dylib", ".o", ".a",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".pyc", ".pyo", ".class", ".jar",
    ".sqlite", ".db",
    ".DS_Store",
})

LOCK_FILES = frozenset({
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
    "Pipfile.lock", "poetry.lock", "uv.lock",
    "Gemfile.lock", "Cargo.lock", "composer.lock",
})


@dataclass
class FileEntry:
    path: Path
    size: int
    extension: str


def _matches_any(name: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(name, p) for p in patterns)


def discover_files(
    paths: list[Path],
    include: list[str] | None = None,
    exclude: list[str] | None = None,
) -> list[FileEntry]:
    """Walk paths and return discoverable text files.

    Args:
        paths: Files or directories to scan.
        include: If set, only files matching these globs are included.
        exclude: Additional glob patterns to exclude.
    """
    results: list[FileEntry] = []
    seen: set[Path] = set()
    exclude = exclude or []

    for root_path in paths:
        root_path = root_path.resolve()
        if root_path.is_file():
            _maybe_add(root_path, include, exclude, seen, results)
        elif root_path.is_dir():
            _walk_dir(root_path, include, exclude, seen, results)

    results.sort(key=lambda f: f.path)
    return results


def _walk_dir(
    directory: Path,
    include: list[str] | None,
    exclude: list[str],
    seen: set[Path],
    results: list[FileEntry],
) -> None:
    try:
        entries = sorted(directory.iterdir())
    except PermissionError:
        return

    for entry in entries:
        if entry.is_dir():
            if entry.name not in DEFAULT_IGNORE_DIRS and not entry.name.startswith("."):
                _walk_dir(entry, include, exclude, seen, results)
        elif entry.is_file():
            _maybe_add(entry, include, exclude, seen, results)


def _maybe_add(
    filepath: Path,
    include: list[str] | None,
    exclude: list[str],
    seen: set[Path],
    results: list[FileEntry],
) -> None:
    resolved = filepath.resolve()
    if resolved in seen:
        return
    seen.add(resolved)

    name = filepath.name
    ext = filepath.suffix.lower()

    # Skip binary files
    if ext in BINARY_EXTENSIONS:
        return

    # Skip lock files
    if name in LOCK_FILES:
        return

    # Apply include filter
    if include and not _matches_any(name, include):
        return

    # Apply exclude filter
    if _matches_any(name, exclude):
        return

    try:
        size = filepath.stat().st_size
    except OSError:
        return

    # Skip empty files
    if size == 0:
        return

    results.append(FileEntry(path=resolved, size=size, extension=ext))
