# tokcount MVP — Implementation Plan

## Summary

Build a CLI tool (`tokcount`) that counts tokens in files/directories for different LLM models, estimates costs, and shows which files consume the most context. Offline only — no API keys required.

## Tasks

1. **Spec Documentation** — Save plan, shape, and references
2. **Project Scaffolding** — uv init, pyproject.toml, directory structure
3. **Model Definitions** — ModelInfo dataclass, model registry (GPT-5, Claude 4.5, Gemini 3)
4. **Tokenizer Abstractions** — TiktokenTokenizer + CharApproxTokenizer
5. **File Discovery** — Recursive walker with ignores, include/exclude globs
6. **Core Counter** — Read files, count tokens, aggregate into CountResult
7. **Rich Table Formatter** — Summary panel, top-N files, extension breakdown
8. **JSON Formatter** — Machine-readable JSON output
9. **CLI Layer** — Typer commands: count (default) + models
10. **Tests and README** — pytest suite + documentation

## Dependency Graph

```
Task 2 (Scaffold)
       |
  +----+----+
  |         |
Task 3    Task 5
  |         |
Task 4      |
  |         |
  +----+----+
       |
  Task 6 (Counter)
       |
  +----+----+
  |         |
Task 7    Task 8
  |         |
  +----+----+
       |
  Task 9 (CLI)
       |
  Task 10 (Tests)
```

## Final Verification

`uv run tokcount . -m gpt-5 -m claude-sonnet-4.5 --top 5`
