"""Barcode-related semantic Faker types."""

from .base import FakerType


class EAN13(FakerType):
    """EAN-13 barcode. Uses Faker provider ``ean13``."""

    faker_provider = "ean13"


class EAN8(FakerType):
    """EAN-8 barcode. Uses Faker provider ``ean8``."""

    faker_provider = "ean8"
