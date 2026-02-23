"""Date/time-related semantic Faker types (string providers)."""

from .base import FakerType


class Date(FakerType):
    faker_provider = "date"


class DateTime(FakerType):
    faker_provider = "iso8601"


class Time(FakerType):
    faker_provider = "time"
