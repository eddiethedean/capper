"""Runnable example for the Getting started user guide.

Run from repo root (with capper installed): python docs/examples/getting_started.py
"""

from pydantic import BaseModel
from capper import Name, Email
from polyfactory.factories.pydantic_factory import ModelFactory


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    pass


if __name__ == "__main__":
    user = UserFactory.build()
    print("Name:", user.name)
    print("Email:", user.email)
