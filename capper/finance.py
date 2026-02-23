"""Finance / credit card semantic Faker types."""

from .base import FakerType


class CreditCardNumber(FakerType):
    """Credit card number string. Uses Faker provider ``credit_card_number``."""

    faker_provider = "credit_card_number"


class CreditCardExpiry(FakerType):
    """Credit card expiry string. Uses Faker provider ``credit_card_expire``."""

    faker_provider = "credit_card_expire"


class CreditCardProvider(FakerType):
    """Credit card provider name. Uses Faker provider ``credit_card_provider``."""

    faker_provider = "credit_card_provider"
