"""Capper: semantic Faker types with automatic Polyfactory integration.

Import types (e.g. ``Name``, ``Email``) and use them in Pydantic models, dataclasses,
or attrs; Polyfactory will generate values via Faker. Use ``seed(n)`` for reproducibility.
"""

from .base import FakerType, faker, seed
from .commerce import Company, Currency, Price, Product
from .date_time import Date, DateTime, Time
from .finance import CreditCardExpiry, CreditCardNumber, CreditCardProvider
from .geo import Address, City, Country
from .internet import Email, IP, URL, UserName
from .person import FirstName, Job, LastName, Name
from .phone import CountryCallingCode, PhoneNumber
from .text import Paragraph, Sentence

__all__ = [
    "Address",
    "City",
    "Company",
    "Country",
    "CountryCallingCode",
    "CreditCardExpiry",
    "CreditCardNumber",
    "CreditCardProvider",
    "Currency",
    "Date",
    "DateTime",
    "Email",
    "FakerType",
    "FirstName",
    "IP",
    "Job",
    "LastName",
    "Name",
    "Paragraph",
    "PhoneNumber",
    "Price",
    "Product",
    "Sentence",
    "Time",
    "URL",
    "UserName",
    "faker",
    "seed",
]
