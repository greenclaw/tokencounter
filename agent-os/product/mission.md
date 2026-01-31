# Product Mission

## Problem

When working with LLM agents, developers lack visibility into token consumption. They need to answer three critical questions before making API calls:

- Will these files fit in the model's context window?
- How much will this API call cost?
- Which files are consuming the most tokens?

There's no simple CLI tool that gives quick, accurate answers across multiple LLM providers.

## Target Users

Developers who work with LLMs — building AI-powered applications, using coding agents, or sending code/documents to language models. Anyone who needs to estimate token counts and costs before hitting an API.

## Solution

`tokcount` is a CLI tool that counts tokens in files and directories for different LLM models, estimates costs, and identifies which files consume the most context. Key differentiators:

- **Multi-model support** — GPT-5 family, Claude 4.5 family, Gemini 3 family with accurate tokenizer mappings
- **Cost estimation** — Real pricing data so developers know what an API call will cost
- **Context window awareness** — Shows what percentage of a model's context window your files consume
- **Beautiful output** — Rich terminal tables with top-N heaviest files, extension breakdowns, and context fit indicators
- **Multi-model comparison** — Compare token counts and costs across models side by side
