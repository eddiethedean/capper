"""Text-related semantic Faker types."""

from .base import FakerType


class Paragraph(FakerType):
    faker_provider = "paragraph"


class Sentence(FakerType):
    faker_provider = "sentence"
