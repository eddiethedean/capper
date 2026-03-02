"""FakerType base class and shared Faker instance with automatic Polyfactory registration.

The module-level ``faker`` is attached to Polyfactory's BaseFactory so that one seed
controls both capper types and built-in types. Use ``seed(n)`` for reproducible data.

Note: The shared ``faker`` and ``use_faker()`` are not thread-safe; do not switch
the global Faker from multiple threads while building models.
"""

from typing import Any

from faker import Faker
from polyfactory.factories.base import BaseFactory

faker = Faker()

# Share this Faker with Polyfactory so one seed controls both capper types and built-in types.
BaseFactory.__faker__ = faker


def seed(seed_value: int) -> None:
    """Seed the shared Faker instance for reproducible data.

    Args:
        seed_value: Integer seed; same value produces the same sequence of values.
    """
    faker.seed_instance(seed_value)


def use_faker(instance: Faker) -> None:
    """Use a custom Faker instance for both Capper and Polyfactory.

    Replaces the module-level faker and Polyfactory's BaseFactory.__faker__
    so that one instance (e.g. a locale-specific Faker) is used everywhere.
    Call before building any models.

    Note: The shared faker is not thread-safe. Do not call use_faker() from
    multiple threads while other threads are building models.

    Args:
        instance: The Faker instance to use (e.g. Faker('de_DE')).
    """
    global faker
    faker = instance
    BaseFactory.__faker__ = instance


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
