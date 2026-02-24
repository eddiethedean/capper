"""Runnable example for the Reproducible data user guide.

Run from repo root (with capper installed): python docs/examples/reproducible_data.py
"""

from capper import seed, Name, Email
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    pass


class UserWithFixedSeed(BaseModel):
    name: Name


class UserWithFixedSeedFactory(ModelFactory[UserWithFixedSeed]):
    __random_seed__ = 12345


if __name__ == "__main__":
    print("--- seed(42) twice => same user ---")
    seed(42)
    user1 = UserFactory.build()
    seed(42)
    user2 = UserFactory.build()
    assert user1.name == user2.name and user1.email == user2.email
    print("Reproducible:", user1.name, user1.email)

    print("\n--- seed() vs seed_random() => same name ---")
    seed(42)
    a = UserFactory.build()
    UserFactory.seed_random(42)
    b = UserFactory.build()
    assert a.name == b.name
    print("Same name:", a.name)

    print("\n--- __random_seed__ on factory ---")
    u1 = UserWithFixedSeedFactory.build()
    u2 = UserWithFixedSeedFactory.build()
    print(u1.name, u2.name)
