"""Phone-related semantic Faker types (phone number, country calling code)."""

from .base import FakerType


class PhoneNumber(FakerType):
    """Phone number string. Uses Faker provider ``phone_number``."""

    faker_provider = "phone_number"


class CountryCallingCode(FakerType):
    """Country calling code. Uses Faker provider ``country_calling_code``."""

    faker_provider = "country_calling_code"
