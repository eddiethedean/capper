"""Example: Pydantic model with capper types and Polyfactory ModelFactory."""

from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory

from capper import Email, Name


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    pass


if __name__ == "__main__":
    user = UserFactory.build()
    print(user.name)   # e.g., "Ashley Johnson"
    print(user.email)  # e.g., "ashley.johnson@example.com"
