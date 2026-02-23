"""FakerType base class with automatic Polyfactory provider registration."""

from typing import Any

from faker import Faker
from polyfactory.factories.base import BaseFactory

faker = Faker()


def _install_pydantic_schema() -> None:
    """If Pydantic is installed, add __get_pydantic_core_schema__ to FakerType."""
    try:
        from pydantic import GetCoreSchemaHandler
        from pydantic_core import CoreSchema, core_schema
    except ImportError:
        return

    def __get_pydantic_core_schema__(
        source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Tell Pydantic to validate as str and coerce to this type."""
        return core_schema.no_info_after_validator_function(source_type, handler(str))

    FakerType.__get_pydantic_core_schema__ = __get_pydantic_core_schema__  # type: ignore[method-assign]


class FakerType(str):
    """Base for semantic Faker types. Subclasses are auto-registered with Polyfactory."""

    faker_provider: str = ""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        provider = getattr(cls, "faker_provider", None)
        if provider:
            _register(cls, provider)


_install_pydantic_schema()


def _register(cls: type, provider_name: str) -> None:
    """Register a FakerType subclass with Polyfactory."""
    BaseFactory.add_provider(
        cls,
        lambda _cls=cls, _name=provider_name: getattr(faker, _name)(),
    )
