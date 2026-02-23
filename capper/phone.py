"""Phone-related semantic Faker types."""

from .base import FakerType


class PhoneNumber(FakerType):
    faker_provider = "phone_number"


class CountryCallingCode(FakerType):
    faker_provider = "country_calling_code"
