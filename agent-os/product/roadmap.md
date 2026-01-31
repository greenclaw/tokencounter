# Product Roadmap

## Phase 1: MVP

- Project setup with uv and Python 3.14
- Model definitions with current pricing (GPT-5 family, Claude 4.5 family, Gemini 3 family)
- Tokenizer wrapper (tiktoken for OpenAI models, character-based approximations for Claude/Gemini)
- File discovery (recursive directory walk, skip binaries, respect ignore patterns)
- Core counter logic aggregating per-file token counts
- CLI with Typer (`tokcount <paths>` and `tokcount models` commands)
- Rich table formatter with summary stats, top-N heaviest files, extension breakdown, context fit check
- JSON formatter for machine-readable output
- Include/exclude glob filters
- Multi-model comparison (`-m model1 -m model2`)
- Basic tests (counter, CLI)
- README with usage examples
- Publish to PyPI

## Phase 2: Post-Launch

- `tokcount serve` — FastAPI web interface for browser-based token counting
- `tokcount --github owner/repo` — Fetch and count tokens in a GitHub repository
- VS Code extension — Token counts inline in the editor
- Watch mode — Re-count on file changes
- Git diff mode — Show tokens added/removed between commits
