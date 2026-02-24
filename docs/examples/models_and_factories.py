"""Runnable example for the Models and factories user guide.

Run from repo root (with capper installed): python docs/examples/models_and_factories.py
"""

from dataclasses import dataclass
from pydantic import BaseModel
from capper import Name, Email, Address, PhoneNumber, Company, Product, Price
from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory


# --- Pydantic ---
class Contact(BaseModel):
    name: Name
    email: Email
    address: Address
    phone: PhoneNumber


class ContactFactory(ModelFactory[Contact]):
    pass


# --- Dataclass ---
@dataclass
class Person:
    name: Name
    email: Email


class PersonFactory(DataclassFactory[Person]):
    pass


# --- Mixed Capper + built-in ---
class Listing(BaseModel):
    company: Company
    product: Product
    price: Price
    quantity: int


class ListingFactory(ModelFactory[Listing]):
    pass


if __name__ == "__main__":
    print("--- Contact (Pydantic) ---")
    contact = ContactFactory.build()
    print(contact.model_dump())
    for c in ContactFactory.batch(2):
        print(c.name, "—", c.email)

    print("\n--- Person (dataclass) ---")
    person = PersonFactory.build()
    print(person.name, person.email)
    for p in PersonFactory.batch(2):
        print(p)

    print("\n--- Listing (Capper + int) ---")
    listing = ListingFactory.build()
    print(f"{listing.company}: {listing.product} @ {listing.price} x {listing.quantity}")
