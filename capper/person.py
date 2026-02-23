"""Person-related semantic Faker types (name, job)."""

from .base import FakerType


class Name(FakerType):
    """Full name. Uses Faker provider ``name``."""

    faker_provider = "name"


class FirstName(FakerType):
    """First/given name. Uses Faker provider ``first_name``."""

    faker_provider = "first_name"


class LastName(FakerType):
    """Last/family name. Uses Faker provider ``last_name``."""

    faker_provider = "last_name"


class Job(FakerType):
    """Job title. Uses Faker provider ``job``."""

    faker_provider = "job"
