"""Commerce-related semantic Faker types."""

from .base import FakerType


class Company(FakerType):
    faker_provider = "company"


class Product(FakerType):
    faker_provider = "catch_phrase"


class Currency(FakerType):
    faker_provider = "currency_code"


class Price(FakerType):
    faker_provider = "pricetag"
