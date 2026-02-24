"""Color-related semantic Faker types."""

from .base import FakerType


class HexColor(FakerType):
    """Hex color string (e.g. #ff5500). Uses Faker provider ``color`` with hex format."""

    faker_provider = "color"
    faker_kwargs = {"color_format": "hex"}
