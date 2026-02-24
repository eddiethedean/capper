"""Capper: semantic Faker types with automatic Polyfactory integration.

Import types (e.g. ``Name``, ``Email``) and use them in Pydantic models, dataclasses,
or attrs; Polyfactory will generate values via Faker. Use ``seed(n)`` for reproducibility.
With Hypothesis installed (pip install capper[hypothesis]), import capper.strategies
and use st.from_type(Name) for property-based tests.
"""

try:
    from importlib.metadata import version as _version

    __version__ = _version("capper")
except Exception:  # Package not installed (e.g. dev tree) or metadata missing
    __version__ = "0.3.0"

from .barcode import EAN8, EAN13
from .base import FakerType, faker, seed, use_faker
from .color import HexColor
from .commerce import Company, Currency, Price, Product
from .date_time import Date, DateTime, Time
from .file import FileExtension, FileName, FilePath
from .finance import CreditCardExpiry, CreditCardNumber, CreditCardProvider
from .geo import Address, City, Country
from .internet import IP, URL, Email, UserName
from .misc import UUID
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
    "EAN13",
    "EAN8",
    "Email",
    "FakerType",
    "FileExtension",
    "FileName",
    "FilePath",
    "FirstName",
    "HexColor",
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
    "UUID",
    "UserName",
    "faker",
    "seed",
    "use_faker",
]
