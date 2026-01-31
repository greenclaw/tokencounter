# Tech Stack

## Language & Runtime

- **Python 3.14** — Latest stable Python
- **uv** — Package manager and project tooling

## CLI Framework

- **Typer** (latest) — CLI framework built on Click, with type hint-driven argument parsing
- **Rich** (latest) — Terminal formatting, tables, progress bars

## Tokenization

All tokenization is offline — no API keys required.

- **tiktoken** (latest) — OpenAI's fast BPE tokenizer library for GPT family models (exact counts)
- **Character approximation for Claude** (~3.5 chars/token) — Anthropic has not released a public offline tokenizer; this is the standard estimation method
- **Character approximation for Gemini** (~4 chars/token) — Google's experimental `LocalTokenizer` exists but is unstable and text-only; character estimation is more reliable for MVP

### Why not API-based counting?

- Anthropic's `count_tokens` API and Google's `count_tokens` API both give exact counts but require API keys and network access
- For a CLI tool that should work instantly without configuration, offline-only is the right trade-off
- tiktoken gives exact counts for OpenAI models, and approximations for Claude/Gemini are sufficient for context window estimation and cost planning

## Build & Distribution

- **Hatchling** — Build backend
- **PyPI** — Package distribution

## Development

- **pytest** (latest) — Testing framework
- **ruff** (latest) — Linter and formatter

## Optional (Post-MVP)

- **FastAPI** (latest) — Web API for `tokcount serve`
- **uvicorn** (latest) — ASGI server
