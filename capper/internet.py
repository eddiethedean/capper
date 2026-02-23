"""Internet-related semantic Faker types."""

from .base import FakerType


class Email(FakerType):
    faker_provider = "email"


class URL(FakerType):
    faker_provider = "url"


class IP(FakerType):
    faker_provider = "ipv4"


class UserName(FakerType):
    faker_provider = "user_name"
