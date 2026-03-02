"""Factory field helpers for Polyfactory-style overrides with Faker kwargs.

Use ``faker_field(Sentence, nb_words=5)`` on a factory class to generate that
field with custom provider arguments, matching how Polyfactory uses callables
and ``Use(...)`` for field overrides.
"""

from __future__ import annotations

from typing import Any, Callable, TypeVar

from .base import FakerType, faker

T = TypeVar("T", bound=FakerType)


def faker_field(type_class: type[T], **kwargs: Any) -> Callable[[], T]:
    """Return a callable for use as a Polyfactory field override with Faker kwargs.

    Assign the result to a factory attribute so that field is generated using
    the given FakerType's provider with the specified keyword arguments.
    Polyfactory invokes the callable at build time. Uses the shared per-thread
    Faker (same as ``seed()`` and ``use_faker()``).

    Example::

        from pydantic import BaseModel
        from polyfactory.factories.pydantic_factory import ModelFactory
        from capper import Sentence, faker_field

        class Post(BaseModel):
            summary: Sentence
            body: Sentence

        class PostFactory(ModelFactory[Post]):
            summary = faker_field(Sentence, nb_words=5)
            body = faker_field(Sentence, nb_words=20)

    Args:
        type_class: A FakerType subclass (e.g. Sentence, Date).
        **kwargs: Keyword arguments passed to the Faker provider (e.g. nb_words=5).

    Returns:
        A no-argument callable that returns an instance of type_class.

    Raises:
        AttributeError: If type_class has no faker_provider or Faker has no such provider.
        TypeError: If the Faker provider is not callable.
    """
    provider = getattr(type_class, "faker_provider", None)
    if not provider:
        raise AttributeError(
            f"{type_class.__name__} has no faker_provider. "
            "Use a Capper type that defines faker_provider (e.g. Sentence, Date)."
        )
    if not hasattr(faker, provider):
        raise AttributeError(
            f"Faker has no provider {provider!r} (used by {type_class.__name__}). "
            "Check faker_provider on the type."
        )
    provider_fn = getattr(faker, provider)
    if not callable(provider_fn):
        raise TypeError(f"Faker.{provider} is not callable (used by {type_class.__name__}).")
    provider_kwargs = dict(getattr(type_class, "faker_kwargs", None) or {})
    provider_kwargs.update(kwargs)

    def _generate() -> T:
        value = provider_fn(**provider_kwargs)
        return type_class(str(value))

    return _generate


__all__ = ["faker_field"]
