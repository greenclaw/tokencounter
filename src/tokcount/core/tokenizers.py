from abc import ABC, abstractmethod

import tiktoken


class Tokenizer(ABC):
    @abstractmethod
    def count(self, text: str) -> int: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def is_exact(self) -> bool: ...


class TiktokenTokenizer(Tokenizer):
    def __init__(self, encoding_name: str) -> None:
        self._encoding_name = encoding_name
        self._enc = tiktoken.get_encoding(encoding_name)

    def count(self, text: str) -> int:
        return len(self._enc.encode(text, disallowed_special=()))

    @property
    def name(self) -> str:
        return f"tiktoken/{self._encoding_name}"

    @property
    def is_exact(self) -> bool:
        return True


class CharApproxTokenizer(Tokenizer):
    def __init__(self, chars_per_token: float, label: str) -> None:
        self._chars_per_token = chars_per_token
        self._label = label

    def count(self, text: str) -> int:
        return max(1, round(len(text) / self._chars_per_token))

    @property
    def name(self) -> str:
        return f"char_approx/{self._label}"

    @property
    def is_exact(self) -> bool:
        return False


# Cached tokenizer instances
_cache: dict[str, Tokenizer] = {}


def get_tokenizer(tokenizer_id: str) -> Tokenizer:
    """Get or create a cached tokenizer instance.

    tokenizer_id is one of:
      - a tiktoken encoding name (e.g. "o200k_base", "o200k_harmony")
      - "char_approx_3.5" (Claude-style)
      - "char_approx_4" (Gemini-style)
    """
    if tokenizer_id in _cache:
        return _cache[tokenizer_id]

    if tokenizer_id.startswith("char_approx_"):
        chars_per_token = float(tokenizer_id.removeprefix("char_approx_"))
        tok = CharApproxTokenizer(chars_per_token, tokenizer_id)
    else:
        tok = TiktokenTokenizer(tokenizer_id)

    _cache[tokenizer_id] = tok
    return tok
