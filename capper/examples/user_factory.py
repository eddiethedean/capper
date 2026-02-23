"""Example: Pydantic model with capper types and Polyfactory ModelFactory.

Run with: python -m capper.examples.user_factory
Output varies each run (Faker generates random data).
"""

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
    print(user.name)
    print(user.email)
