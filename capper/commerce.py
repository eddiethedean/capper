"""Commerce-related semantic Faker types (company, product, currency, price)."""

from .base import FakerType


class Company(FakerType):
    """Company name. Uses Faker provider ``company``."""

    faker_provider = "company"


class Product(FakerType):
    """Product/catch phrase. Uses Faker provider ``catch_phrase``."""

    faker_provider = "catch_phrase"


class Currency(FakerType):
    """Currency code. Uses Faker provider ``currency_code``."""

    faker_provider = "currency_code"


class Price(FakerType):
    """Price tag string. Uses Faker provider ``pricetag``."""

    faker_provider = "pricetag"
