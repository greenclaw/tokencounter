from dataclasses import dataclass


@dataclass(frozen=True)
class ModelInfo:
    name: str
    provider: str
    context_window: int
    input_price_per_mtok: float  # USD per 1M input tokens
    output_price_per_mtok: float  # USD per 1M output tokens
    tokenizer: str  # e.g. "o200k_base", "char_approx_3.5"
    aliases: tuple[str, ...] = ()


# --- Model Registry ---

_MODELS: dict[str, ModelInfo] = {}
_ALIASES: dict[str, str] = {}

DEFAULT_MODEL = "claude-sonnet-4.5"


def _register(model: ModelInfo) -> None:
    _MODELS[model.name] = model
    for alias in model.aliases:
        _ALIASES[alias] = model.name


# OpenAI GPT-5 family
_register(ModelInfo(
    name="gpt-5",
    provider="OpenAI",
    context_window=256_000,
    input_price_per_mtok=2.00,
    output_price_per_mtok=8.00,
    tokenizer="o200k_harmony",
    aliases=("gpt5",),
))
_register(ModelInfo(
    name="gpt-5.2",
    provider="OpenAI",
    context_window=256_000,
    input_price_per_mtok=2.50,
    output_price_per_mtok=10.00,
    tokenizer="o200k_harmony",
    aliases=("gpt5.2",),
))
_register(ModelInfo(
    name="gpt-5-pro",
    provider="OpenAI",
    context_window=256_000,
    input_price_per_mtok=5.00,
    output_price_per_mtok=20.00,
    tokenizer="o200k_harmony",
    aliases=("gpt5-pro",),
))
_register(ModelInfo(
    name="gpt-5-mini",
    provider="OpenAI",
    context_window=256_000,
    input_price_per_mtok=0.30,
    output_price_per_mtok=1.20,
    tokenizer="o200k_harmony",
    aliases=("gpt5-mini",),
))
_register(ModelInfo(
    name="gpt-5-nano",
    provider="OpenAI",
    context_window=128_000,
    input_price_per_mtok=0.10,
    output_price_per_mtok=0.40,
    tokenizer="o200k_harmony",
    aliases=("gpt5-nano",),
))
_register(ModelInfo(
    name="gpt-5-codex",
    provider="OpenAI",
    context_window=256_000,
    input_price_per_mtok=3.00,
    output_price_per_mtok=12.00,
    tokenizer="o200k_harmony",
    aliases=("codex",),
))
_register(ModelInfo(
    name="gpt-4o",
    provider="OpenAI",
    context_window=128_000,
    input_price_per_mtok=2.50,
    output_price_per_mtok=10.00,
    tokenizer="o200k_base",
    aliases=("4o",),
))

# Anthropic Claude 4.5 family
_register(ModelInfo(
    name="claude-opus-4.5",
    provider="Anthropic",
    context_window=200_000,
    input_price_per_mtok=15.00,
    output_price_per_mtok=75.00,
    tokenizer="char_approx_3.5",
    aliases=("opus", "opus-4.5"),
))
_register(ModelInfo(
    name="claude-sonnet-4.5",
    provider="Anthropic",
    context_window=200_000,
    input_price_per_mtok=3.00,
    output_price_per_mtok=15.00,
    tokenizer="char_approx_3.5",
    aliases=("sonnet", "sonnet-4.5"),
))
_register(ModelInfo(
    name="claude-haiku-4.5",
    provider="Anthropic",
    context_window=200_000,
    input_price_per_mtok=0.80,
    output_price_per_mtok=4.00,
    tokenizer="char_approx_3.5",
    aliases=("haiku", "haiku-4.5"),
))

# Google Gemini 3 family
_register(ModelInfo(
    name="gemini-3-pro",
    provider="Google",
    context_window=2_000_000,
    input_price_per_mtok=1.25,
    output_price_per_mtok=10.00,
    tokenizer="char_approx_4",
    aliases=("gemini-pro", "gemini3-pro"),
))
_register(ModelInfo(
    name="gemini-3-flash",
    provider="Google",
    context_window=1_000_000,
    input_price_per_mtok=0.15,
    output_price_per_mtok=0.60,
    tokenizer="char_approx_4",
    aliases=("gemini-flash", "gemini3-flash"),
))


def get_model(name_or_alias: str) -> ModelInfo:
    """Look up a model by name or alias. Raises KeyError if not found."""
    canonical = _ALIASES.get(name_or_alias, name_or_alias)
    if canonical in _MODELS:
        return _MODELS[canonical]
    raise KeyError(f"Unknown model: {name_or_alias!r}")


def get_default_model() -> ModelInfo:
    return _MODELS[DEFAULT_MODEL]


def list_models() -> list[ModelInfo]:
    """Return all registered models, sorted by provider then name."""
    return sorted(_MODELS.values(), key=lambda m: (m.provider, m.name))
