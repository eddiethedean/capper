"""FakerType base class and per-thread Faker proxy with automatic Polyfactory registration.

The module-level ``faker`` is a proxy to a per-thread Faker instance. Each thread has its own
Faker; ``seed(n)`` and ``use_faker(instance)`` only affect the current thread. Polyfactory's
BaseFactory.__faker__ is set to the same proxy, so one seed per thread controls both capper
types and built-in types. Thread-safe for concurrent use from multiple threads.
"""

import threading
from typing import Any, cast

from faker import Faker
from polyfactory.factories.base import BaseFactory

_faker_local = threading.local()


def _get_faker() -> Faker:
    """Return the current thread's Faker instance, creating one if needed."""
    try:
        instance = _faker_local.current
    except AttributeError:
        instance = None
    if instance is None:
        instance = Faker()
        _faker_local.current = instance
    return cast(Faker, instance)


class _FakerProxy:
    """Proxy that forwards all attribute access to the current thread's Faker."""

    __slots__ = ()

    def __getattr__(self, name: str) -> Any:
        return getattr(_get_faker(), name)


# Single process-wide proxy; each thread gets its own Faker via _get_faker().
faker: Faker = _FakerProxy()  # type: ignore[assignment]
BaseFactory.__faker__ = faker


def seed(seed_value: int) -> None:
    """Seed the current thread's Faker instance for reproducible data.

    Args:
        seed_value: Integer seed; same value produces the same sequence of values.
    """
    _get_faker().seed_instance(seed_value)


def use_faker(instance: Faker | None) -> None:
    """Use a custom Faker instance for the current thread only.

    Sets the Faker used by Capper and Polyfactory for this thread (e.g. a
    locale-specific Faker). Other threads are unaffected. Call before building
    any models in this thread. Pass None to reset this thread to a new default
    Faker (e.g. after temporarily using a custom instance).

    Args:
        instance: The Faker instance to use (e.g. Faker('de_DE')), or None to reset.
    """
    if instance is None or instance is faker:
        try:
            del _faker_local.current
        except AttributeError:
            pass
    else:
        _faker_local.current = instance


def _install_pydantic_schema() -> None:
    """If Pydantic is available, attach __get_pydantic_core_schema__ to FakerType."""
    try:
        from pydantic import GetCoreSchemaHandler
        from pydantic_core import CoreSchema, core_schema
    except ImportError:
        return

    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Validate as str then coerce to the FakerType subclass."""
        return core_schema.no_info_after_validator_function(cls, handler(str))

    FakerType.__get_pydantic_core_schema__ = classmethod(__get_pydantic_core_schema__)  # type: ignore[attr-defined]


class FakerType(str):
    """Base class for semantic Faker types; subclasses auto-register with Polyfactory.

    Subclasses must set a non-empty ``faker_provider`` (the Faker method name).
    Optional ``faker_kwargs`` is a dict of keyword arguments passed to that provider
    (e.g. ``faker_kwargs = {"nb_words": 10}`` for ``sentence``).
    When Hypothesis is installed, use ``st.from_type(YourFakerType)`` for property-based tests.
    """

    faker_provider: str = ""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        provider = getattr(cls, "faker_provider", None)
        if provider:
            _register(cls, provider)


_install_pydantic_schema()


def _register(cls: type[FakerType], provider_name: str) -> None:
    """Register a FakerType subclass with Polyfactory so factories can generate values."""
    if not hasattr(faker, provider_name):
        raise AttributeError(
            f"Faker has no provider {provider_name!r} (used by {cls.__name__}). "
            "Check faker_provider on the type."
        )
    provider_fn = getattr(faker, provider_name)
    if not callable(provider_fn):
        raise TypeError(f"Faker.{provider_name} is not callable (used by {cls.__name__}).")
    provider_kwargs = dict(getattr(cls, "faker_kwargs", None) or {})

    def _provide() -> str:
        value = getattr(faker, provider_name)(**provider_kwargs)
        return str(value)

    BaseFactory.add_provider(cls, _provide)
