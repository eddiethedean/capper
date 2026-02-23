"""FakerType base class with automatic Polyfactory provider registration."""

from typing import Any

from faker import Faker
from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from polyfactory.factories.base import BaseFactory

faker = Faker()


class FakerType(str):
    """Base for semantic Faker types. Subclasses are auto-registered with Polyfactory."""

    faker_provider: str = ""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        provider = getattr(cls, "faker_provider", None)
        if provider:
            _register(cls, provider)

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        """Tell Pydantic to validate as str and coerce to this type."""
        return core_schema.no_info_after_validator_function(cls, handler(str))


def _register(cls: type, provider_name: str) -> None:
    """Register a FakerType subclass with Polyfactory."""
    BaseFactory.add_provider(
        cls,
        lambda _cls=cls, _name=provider_name: getattr(faker, _name)(),
    )
