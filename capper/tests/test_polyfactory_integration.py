"""Tests for Pydantic + ModelFactory + capper types integration."""

import pytest
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory

from capper import Email, Name


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    pass


def test_user_factory_builds_with_capper_types() -> None:
    """ModelFactory builds a User with Name and Email filled by Faker."""
    user = UserFactory.build()
    assert isinstance(user.name, (str, Name))
    assert isinstance(user.email, (str, Email))
    assert len(user.name) > 0
    assert "@" in user.email


def test_user_factory_builds_batch() -> None:
    """ModelFactory.batch produces multiple users."""
    users = UserFactory.batch(3)
    assert len(users) == 3
    for user in users:
        assert isinstance(user, User)
        assert len(user.name) > 0
        assert "@" in user.email


def test_capper_types_auto_registered_with_polyfactory() -> None:
    """Importing capper registers all public types; Polyfactory can build models using them."""
    from capper import PhoneNumber
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    class Contact(BaseModel):
        phone: PhoneNumber

    class ContactFactory(ModelFactory[Contact]):
        pass

    contact = ContactFactory.build()
    assert isinstance(contact.phone, (str, PhoneNumber))
    assert len(contact.phone) > 0
