# tokcount

Count tokens in files and directories for different LLM models. Estimates costs and shows which files consume the most context. Offline only — no API keys required.

## Installation

```bash
uv tool install .
```

Or run directly:

```bash
uv run tokcount count . -m gpt-5
```

## Quick Start

```bash
# Count tokens with default model (claude-sonnet-4.5)
tokcount count .

# Compare multiple models
tokcount count src/ -m gpt-5 -m claude-sonnet-4.5 -m gemini-flash

# Show top 20 files, JSON output
tokcount count . --top 20 --format json

# Only Python files, exclude tests
tokcount count . --include "*.py" --exclude "test_*"
```

## CLI Reference

### `tokcount count <paths>`

Count tokens in files and directories.

| Option | Description |
|---|---|
| `--model, -m` | Model to count for (repeatable). Default: `claude-sonnet-4.5` |
| `--format, -f` | Output format: `table` or `json`. Default: `table` |
| `--top, -t` | Number of top files to show. Default: `10` |
| `--include` | Include only files matching these globs (repeatable) |
| `--exclude` | Exclude files matching these globs (repeatable) |

### `tokcount models [name]`

List all supported models or show detail for a specific model.

```bash
tokcount models          # list all
tokcount models gpt-5    # show detail
```

## Supported Models

| Model | Provider | Context | Tokenizer |
|---|---|---|---|
| gpt-5, gpt-5.2, gpt-5-pro | OpenAI | 256K | tiktoken (exact) |
| gpt-5-mini | OpenAI | 256K | tiktoken (exact) |
| gpt-5-nano, gpt-4o | OpenAI | 128K | tiktoken (exact) |
| claude-opus-4.5 | Anthropic | 200K | char approx (~3.5 c/t) |
| claude-sonnet-4.5 | Anthropic | 200K | char approx (~3.5 c/t) |
| claude-haiku-4.5 | Anthropic | 200K | char approx (~3.5 c/t) |
| gemini-3-pro | Google | 2M | char approx (~4 c/t) |
| gemini-3-flash | Google | 1M | char approx (~4 c/t) |

Models also accept short aliases (e.g., `sonnet`, `haiku`, `opus`, `gemini-flash`).

## Tokenization

- **OpenAI models**: Exact counts via [tiktoken](https://github.com/openai/tiktoken)
- **Claude models**: Approximation at ~3.5 characters per token
- **Gemini models**: Approximation at ~4 characters per token

Approximate counts are marked as such in the output.

## Default Ignores

The following are ignored by default: `.git`, `node_modules`, `__pycache__`, `.venv`, `dist`, `build`, binary files (images, archives, executables), and lock files (`package-lock.json`, `uv.lock`, etc.).

## License

MIT
