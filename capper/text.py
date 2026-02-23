"""Text-related semantic Faker types (paragraph, sentence)."""

from .base import FakerType


class Paragraph(FakerType):
    """Paragraph of text. Uses Faker provider ``paragraph``."""

    faker_provider = "paragraph"


class Sentence(FakerType):
    """Single sentence. Uses Faker provider ``sentence``."""

    faker_provider = "sentence"
