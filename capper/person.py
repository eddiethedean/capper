"""Person-related semantic Faker types."""

from .base import FakerType


class Name(FakerType):
    faker_provider = "name"


class FirstName(FakerType):
    faker_provider = "first_name"


class LastName(FakerType):
    faker_provider = "last_name"
