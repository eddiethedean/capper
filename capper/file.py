"""File-related semantic Faker types (path, name, extension)."""

from .base import FakerType


class FilePath(FakerType):
    """File path. Uses Faker provider ``file_path``."""

    faker_provider = "file_path"


class FileName(FakerType):
    """File name with extension. Uses Faker provider ``file_name``."""

    faker_provider = "file_name"


class FileExtension(FakerType):
    """File extension. Uses Faker provider ``file_extension``."""

    faker_provider = "file_extension"
