# tokcount MVP — Shape

## What it is

A CLI tool that counts tokens in files and directories for different LLM models, estimates costs, and identifies which files consume the most context window.

## Scope

### In scope
- Token counting for files/directories
- Multiple model support (GPT-5, Claude 4.5, Gemini 3 families)
- Cost estimation based on model pricing
- Context window usage percentage
- Table (Rich) and JSON output formats
- Include/exclude glob patterns
- Default ignore patterns (node_modules, .git, binaries, etc.)
- Multi-model comparison in single run

### Out of scope
- API-based token counting (offline only)
- Streaming/watch mode
- Configuration files
- Plugin system
- Output token estimation
- Prompt template analysis

## Key Decisions

1. **Tokenization strategy**: Use tiktoken for OpenAI models (exact), character approximation for Claude (~3.5 chars/token) and Gemini (~4 chars/token). This keeps the tool offline and dependency-light.

2. **CLI framework**: Typer — type-hint-driven, minimal boilerplate, good help text generation.

3. **Output**: Rich for terminal tables, stdlib json for machine output. No intermediate template layer.

4. **Build system**: Hatchling via uv. Single pyproject.toml, no setup.py.

5. **Model registry**: Hardcoded dataclass registry. No external config files — models change rarely enough that a code release is fine.

6. **Default model**: claude-sonnet-4.5 — most commonly used model for coding tasks.

## Context

This tool helps developers understand how much of their codebase fits in an LLM's context window before they start a session. Common use case: "Will this repo fit in Claude's context? What should I exclude?"
