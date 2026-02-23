"""FakerType base class and shared Faker instance with automatic Polyfactory registration.

The module-level ``faker`` is attached to Polyfactory's BaseFactory so that one seed
controls both capper types and built-in types. Use ``seed(n)`` for reproducible data.
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


def _install_pydantic_schema() -> None:
    """If Pydantic is available, attach __get_pydantic_core_schema__ to FakerType."""
    try:
        from pydantic import GetCoreSchemaHandler
        from pydantic_core import CoreSchema, core_schema
    except ImportError:
        return

    def __get_pydantic_core_schema__(
        source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Validate as str then coerce to the FakerType subclass."""
        return core_schema.no_info_after_validator_function(source_type, handler(str))

    FakerType.__get_pydantic_core_schema__ = __get_pydantic_core_schema__  # type: ignore[attr-defined]


class FakerType(str):
    """Base class for semantic Faker types; subclasses are auto-registered with Polyfactory.

    Subclasses must set a non-empty ``faker_provider`` (the Faker method name).
    Optional ``faker_kwargs`` is a dict of keyword arguments passed to that provider
    (e.g. ``faker_kwargs = {"nb_words": 10}`` for ``sentence``).
    """

    faker_provider: str = ""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        provider = getattr(cls, "faker_provider", None)
        if provider:
            _register(cls, provider)


_install_pydantic_schema()


def _register(cls: type, provider_name: str) -> None:
    """Register a FakerType subclass with Polyfactory so factories can generate values."""
    provider_kwargs = getattr(cls, "faker_kwargs", None) or {}

    def _provide() -> str:
        return getattr(faker, provider_name)(**provider_kwargs)

    BaseFactory.add_provider(cls, _provide)
