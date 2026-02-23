"""Internet-related semantic Faker types (email, URL, IP, username)."""

from .base import FakerType


class Email(FakerType):
    """Email address. Uses Faker provider ``email``."""

    faker_provider = "email"


class URL(FakerType):
    """URL. Uses Faker provider ``url``."""

    faker_provider = "url"


class IP(FakerType):
    """IPv4 address. Uses Faker provider ``ipv4``."""

    faker_provider = "ipv4"


class UserName(FakerType):
    """Username. Uses Faker provider ``user_name``."""

    faker_provider = "user_name"
