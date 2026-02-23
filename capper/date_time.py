"""Date/time-related semantic Faker types (date, datetime, time as strings)."""

from .base import FakerType


class Date(FakerType):
    """Date string. Uses Faker provider ``date``."""

    faker_provider = "date"


class DateTime(FakerType):
    """ISO 8601 datetime string. Uses Faker provider ``iso8601``."""

    faker_provider = "iso8601"


class Time(FakerType):
    """Time string. Uses Faker provider ``time``."""

    faker_provider = "time"
