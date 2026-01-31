import pytest

from tokcount.core.models import get_default_model, get_model, list_models


def test_get_model_by_name():
    model = get_model("gpt-5")
    assert model.name == "gpt-5"
    assert model.provider == "OpenAI"


def test_get_model_by_alias():
    model = get_model("sonnet")
    assert model.name == "claude-sonnet-4.5"


def test_get_model_unknown():
    with pytest.raises(KeyError, match="Unknown model"):
        get_model("nonexistent-model")


def test_get_default_model():
    model = get_default_model()
    assert model.name == "claude-sonnet-4.5"


def test_list_models_not_empty():
    models = list_models()
    assert len(models) > 0


def test_list_models_sorted_by_provider():
    models = list_models()
    providers = [m.provider for m in models]
    assert providers == sorted(providers)


def test_all_models_have_positive_context_window():
    for model in list_models():
        assert model.context_window > 0, f"{model.name} has invalid context window"


def test_all_models_have_positive_pricing():
    for model in list_models():
        assert model.input_price_per_mtok >= 0, f"{model.name} has negative input price"
        assert model.output_price_per_mtok >= 0, f"{model.name} has negative output price"


def test_all_aliases_resolve():
    for model in list_models():
        for alias in model.aliases:
            resolved = get_model(alias)
            assert resolved.name == model.name
