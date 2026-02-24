"""Miscellaneous semantic Faker types (e.g. UUID)."""

from .base import FakerType


class UUID(FakerType):
    """UUID v4 string. Uses Faker provider ``uuid4``."""

    faker_provider = "uuid4"
