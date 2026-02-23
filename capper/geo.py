"""Geography-related semantic Faker types (address, city, country)."""

from .base import FakerType


class Address(FakerType):
    """Street address. Uses Faker provider ``address``."""

    faker_provider = "address"


class City(FakerType):
    """City name. Uses Faker provider ``city``."""

    faker_provider = "city"


class Country(FakerType):
    """Country name. Uses Faker provider ``country``."""

    faker_provider = "country"
