"""Runnable example for the FastAPI and Pydantic user guide.

Run from repo root (with capper installed): python docs/examples/fastapi_pydantic.py
"""

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from capper import Email, Name


class UserCreate(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[UserCreate]):
    """Factory for API-style payloads."""

    __random_seed__ = 42


if __name__ == "__main__":
    print("--- Single payload ---")
    one = UserFactory.build()
    print(one.model_dump())

    print("\n--- Batch of 3 ---")
    for user in UserFactory.batch(3):
        print(user.model_dump())
