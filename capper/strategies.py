"""Hypothesis strategies for Capper types (optional; requires hypothesis>=6.0).

Use ``st.from_type(Name)`` after importing capper and capper.strategies, or call
``strategies.for_type(Name)`` to get a strategy that generates instances of that type.
"""

from __future__ import annotations

from typing import Type, TypeVar, cast

from hypothesis import strategies as st

import capper

from .base import FakerType, faker
from .registry import build_type_registry

T = TypeVar("T", bound=FakerType)

# All built-in FakerType subclasses for registration, discovered from the public API.
_BUILTIN_TYPES: tuple[type[FakerType], ...] = tuple(build_type_registry(capper).values())


def for_type(cls: Type[T]) -> st.SearchStrategy[T]:
    """Return a Hypothesis strategy that generates instances of the given FakerType subclass."""
    provider = getattr(cls, "faker_provider", None)
    if not provider:
        raise ValueError(f"{cls.__name__} has no faker_provider")
    if not hasattr(faker, provider):
        raise AttributeError(
            f"Faker has no provider {provider!r} (used by {cls.__name__}). "
            "Check faker_provider on the type."
        )
    if not callable(getattr(faker, provider)):
        raise TypeError(f"Faker.{provider} is not callable (used by {cls.__name__}).")
    kwargs = getattr(cls, "faker_kwargs", None) or {}

    @st.composite
    def _draw(draw: st.DrawFn) -> T:
        seed_val = draw(st.integers(min_value=0, max_value=2**32 - 1))
        faker.seed_instance(seed_val)
        value = getattr(faker, provider)(**kwargs)
        return cls(str(value))

    return cast(st.SearchStrategy[T], _draw())


def _register_strategies() -> None:
    """Register all built-in Capper types with Hypothesis so st.from_type() works."""
    from hypothesis.strategies import register_type_strategy

    for typ in _BUILTIN_TYPES:
        register_type_strategy(typ, for_type(typ))


_register_strategies()

__all__ = ["for_type"]
