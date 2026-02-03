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

## Example Output

```
$ tokcount count . --top 5
╭───────────────────────────────────── Token Count ──────────────────────────────────────╮
│ claude-sonnet-4.5 (Anthropic)                                                          │
│ Tokens: 13.7K (approx)  |  Files: 24  |  Size: 47.9 KB                                │
│ Context: 6.8% of 200.0K  |  Cost: $0.0410                                              │
│ Tokenizer: char_approx/char_approx_3.5                                                 │
╰────────────────────────────────────────────────────────────────────────────────────────╯
                       Top 5 Files by Token Count
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ File                             ┃ Tokens ┃      % of Total ┃   Size ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ .gitignore                       │   1.3K │ █░░░░░░░░░ 9.8% │ 4.7 KB │
│ src/tokcount/cli.py              │   1.2K │ █░░░░░░░░░ 8.8% │ 4.2 KB │
│ src/tokcount/core/models.py      │   1.1K │ █░░░░░░░░░ 8.3% │ 4.0 KB │
│ src/tokcount/formatters/table.py │   1.1K │ █░░░░░░░░░ 8.3% │ 4.0 KB │
│ src/tokcount/utils/files.py      │    973 │ █░░░░░░░░░ 7.1% │ 3.4 KB │
└──────────────────────────────────┴────────┴─────────────────┴────────┘
               By Extension
┏━━━━━━━━━━┳━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃ Ext      ┃ Files ┃ Tokens ┃ % of Total ┃
┡━━━━━━━━━━╇━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ .py      │    13 │   8.9K │      65.3% │
│ .md      │     7 │   2.9K │      21.4% │
│ (no ext) │     2 │   1.6K │      12.0% │
│ .toml    │     1 │    173 │       1.3% │
│ .yml     │     1 │      8 │       0.1% │
└──────────┴───────┴────────┴────────────┘
```

Compare multiple models side by side with `-m`:

```bash
tokcount count src/ -m gpt-5 -m sonnet -m gemini-pro
```

Each model gets its own summary panel, top files table, and extension breakdown.

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
