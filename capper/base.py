"""FakerType base class and per-thread Faker proxy with automatic Polyfactory registration.

The module-level ``faker`` is a proxy to a per-thread Faker instance. Each thread has its own
Faker; ``seed(n)`` and ``use_faker(instance)`` only affect the current thread. Polyfactory's
BaseFactory.__faker__ is set to the same proxy, so one seed per thread controls both capper
types and built-in types. Thread-safe for concurrent use from multiple threads.
"""

import threading
import warnings
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
    """Proxy that forwards attribute access to the current thread's Faker.

    ``capper.faker`` is not a concrete ``Faker`` instance: ``isinstance(capper.faker, Faker)``
    is false and the object cannot be pickled as a Faker. Attribute access (including provider
    methods and ``seed_instance``) is delegated to the current thread's instance from
    ``_get_faker()``. Pass ``None`` or ``capper.faker`` to ``use_faker()`` to reset the
    thread-local instance.
    """

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

    Raises:
        TypeError: If seed_value is not an int.
    """
    if not isinstance(seed_value, int):
        raise TypeError(f"seed() requires an int, got {type(seed_value).__name__}")
    _get_faker().seed_instance(seed_value)


def use_faker(instance: Faker | None) -> None:
    """Use a custom Faker instance for the current thread only.

    Sets the Faker used by Capper and Polyfactory for this thread (e.g. a
    locale-specific Faker). Other threads are unaffected. Call before building
    any models in this thread. Pass None to reset this thread to a new default
    Faker (e.g. after temporarily using a custom instance).

    Args:
        instance: The Faker instance to use (e.g. Faker('de_DE')), or None to reset.

    Raises:
        TypeError: If instance is not None, not the capper faker proxy, and not a Faker.
    """
    if instance is None or instance is faker:
        try:
            del _faker_local.current
        except AttributeError:
            pass
    elif isinstance(instance, Faker):
        _faker_local.current = instance
    else:
        raise TypeError(
            f"use_faker() requires a Faker instance or None, got {type(instance).__name__}"
        )


def _install_pydantic_schema() -> None:
    """If Pydantic is available, attach __get_pydantic_core_schema__ to FakerType."""
    try:
        from pydantic import GetCoreSchemaHandler
        from pydantic_core import CoreSchema, core_schema
    except ImportError:
        return  # pragma: no cover — pydantic not installed

    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Validate as str then coerce to the FakerType subclass.

        FakerType subclasses are nominal wrappers: any string passes validation and is
        wrapped as the annotated type. They do not enforce Faker output formats (e.g.
        email shape) on manually supplied values.
        """
        return core_schema.no_info_after_validator_function(cls, handler(str))

    FakerType.__get_pydantic_core_schema__ = classmethod(__get_pydantic_core_schema__)  # type: ignore[attr-defined]


class FakerType(str):
    """Base class for semantic Faker types; subclasses auto-register with Polyfactory.

    Subclasses must set a non-empty ``faker_provider`` (the Faker method name).
    Optional ``faker_kwargs`` is a dict of keyword arguments passed to that provider
    (e.g. ``faker_kwargs = {"nb_words": 10}`` for ``sentence``).
    When Hypothesis is installed, use ``st.from_type(YourFakerType)`` for property-based tests.

    FakerType subclasses are **nominal** string types: they distinguish fields in models
    and factories but do not validate string format when values are supplied manually
    (e.g. via Pydantic ``model_validate``).
    """

    faker_provider: str = ""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        provider = getattr(cls, "faker_provider", None)
        if provider is None or provider == "":
            raise ValueError(
                f"{cls.__name__} has no faker_provider. "
                "Set a non-empty faker_provider on FakerType subclasses."
            )
        if not isinstance(provider, str):
            raise TypeError(
                f"{cls.__name__}.faker_provider must be a non-empty str, "
                f"got {type(provider).__name__}"
            )
        _register(cls, provider)


_install_pydantic_schema()


def _register(cls: type[FakerType], provider_name: str) -> None:
    """Register a FakerType subclass with Polyfactory so factories can generate values."""
    if not isinstance(provider_name, str) or not provider_name:
        raise ValueError(
            f"{cls.__name__} has no faker_provider. "
            "Set a non-empty faker_provider on FakerType subclasses."
        )
    if not hasattr(faker, provider_name):
        raise AttributeError(
            f"Faker has no provider {provider_name!r} (used by {cls.__name__}). "
            "Check faker_provider on the type."
        )
    provider_fn = getattr(faker, provider_name)
    if not callable(provider_fn):
        raise TypeError(f"Faker.{provider_name} is not callable (used by {cls.__name__}).")
    if cls in BaseFactory._providers:
        warnings.warn(
            f"Re-registering Polyfactory provider for {cls.__name__}; "
            "the previous provider is replaced.",
            stacklevel=3,
        )
    provider_kwargs = dict(getattr(cls, "faker_kwargs", None) or {})

    def _provide() -> FakerType:
        value = getattr(faker, provider_name)(**provider_kwargs)
        return cls(str(value))

    BaseFactory.add_provider(cls, _provide)
