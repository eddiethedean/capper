"""Finance / credit card semantic Faker types."""

from .base import FakerType


class CreditCardNumber(FakerType):
    faker_provider = "credit_card_number"


class CreditCardExpiry(FakerType):
    faker_provider = "credit_card_expire"


class CreditCardProvider(FakerType):
    faker_provider = "credit_card_provider"
