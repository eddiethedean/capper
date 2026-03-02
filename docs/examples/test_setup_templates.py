"""Runnable example for the Test setup templates user guide.

Run from repo root (with capper installed): python docs/examples/test_setup_templates.py
"""

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from capper import Email, Name, seed


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    __random_seed__ = 999


if __name__ == "__main__":
    print("--- Using factory-level seed ---")
    one = UserFactory.build()
    two = UserFactory.build()
    print(one.model_dump())
    print(two.model_dump())

    print("\n--- Overriding with global seed() ---")
    seed(42)
    a = UserFactory.build()
    seed(42)
    b = UserFactory.build()
    print(a.model_dump())
    print(b.model_dump())
