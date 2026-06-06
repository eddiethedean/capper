"""Hypothesis strategies for Capper types (optional; requires hypothesis>=6.0).

Use ``st.from_type(Name)`` after importing capper and capper.strategies, or call
``strategies.for_type(Name)`` to get a strategy that generates instances of that type.
"""

from __future__ import annotations

from typing import Type, TypeVar, cast

try:
    from hypothesis import strategies as st
except ImportError as exc:
    raise ImportError(
        "capper.strategies requires hypothesis. Install with: pip install 'capper[hypothesis]'"
    ) from exc

from faker import Faker

import capper

from .base import FakerType
from .registry import build_type_registry

T = TypeVar("T", bound=FakerType)

# All built-in FakerType subclasses for registration, discovered from the public API.
_BUILTIN_TYPES: tuple[type[FakerType], ...] = tuple(build_type_registry(capper).values())


def for_type(cls: Type[T]) -> st.SearchStrategy[T]:
    """Return a Hypothesis strategy that generates instances of the given FakerType subclass."""
    provider = getattr(cls, "faker_provider", None)
    if not provider:
        raise ValueError(f"{cls.__name__} has no faker_provider")
    if not isinstance(provider, str):
        raise TypeError(
            f"{cls.__name__}.faker_provider must be a non-empty str, got {type(provider).__name__}"
        )
    kwargs = dict(getattr(cls, "faker_kwargs", None) or {})
    probe = Faker()
    if not hasattr(probe, provider):
        raise AttributeError(
            f"Faker has no provider {provider!r} (used by {cls.__name__}). "
            "Check faker_provider on the type."
        )
    if not callable(getattr(probe, provider)):
        raise TypeError(f"Faker.{provider} is not callable (used by {cls.__name__}).")

    @st.composite
    def _draw(draw: st.DrawFn) -> T:
        seed_val = draw(st.integers(min_value=0, max_value=2**32 - 1))
        local_faker = Faker()
        local_faker.seed_instance(seed_val)
        value = getattr(local_faker, provider)(**kwargs)
        return cls(str(value))

    return cast(st.SearchStrategy[T], _draw())


def _register_strategies() -> None:
    """Register all built-in Capper types with Hypothesis so st.from_type() works."""
    from hypothesis.strategies import register_type_strategy

    for typ in _BUILTIN_TYPES:
        register_type_strategy(typ, for_type(typ))


_register_strategies()

__all__ = ["for_type"]
