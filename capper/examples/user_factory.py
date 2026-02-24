"""Example: Pydantic model with capper types and Polyfactory ModelFactory.

Run: python -m capper.examples.user_factory
Output varies each run; use capper.seed(n) for reproducible data.
"""

from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from capper import Email, Name


class User(BaseModel):
    """Example Pydantic model with capper types."""

    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    """Polyfactory factory for User; uses capper's Faker for name and email."""

    pass


if __name__ == "__main__":
    user = UserFactory.build()
    print(user.name)
    print(user.email)
