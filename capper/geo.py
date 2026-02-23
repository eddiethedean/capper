"""Geography-related semantic Faker types."""

from .base import FakerType


class Address(FakerType):
    faker_provider = "address"


class City(FakerType):
    faker_provider = "city"


class Country(FakerType):
    faker_provider = "country"
