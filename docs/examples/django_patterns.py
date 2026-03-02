"""Runnable example for the Django-style patterns user guide.

Run from repo root (with capper installed): python docs/examples/django_patterns.py

This example mirrors how you would build schemas and factories in a Django
project without importing Django itself.
"""

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from capper import Email, Name


class UserSchema(BaseModel):
    name: Name
    email: Email


class UserSchemaFactory(ModelFactory[UserSchema]):
    __random_seed__ = 123


if __name__ == "__main__":
    schema = UserSchemaFactory.build()
    print("UserSchema:", schema.model_dump())

    print("\n--- Batch ---")
    for s in UserSchemaFactory.batch(2):
        print(s.model_dump())
