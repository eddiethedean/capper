"""Tests for Polyfactory: ModelFactory, DataclassFactory, shared Faker, auto-registration."""

from dataclasses import dataclass

from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from capper import Email, Name


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    pass


def test_user_factory_builds_with_capper_types() -> None:
    """Builds a User with Name and Email via ModelFactory; asserts non-empty and valid email."""
    user = UserFactory.build()
    assert isinstance(user.name, (str, Name))
    assert isinstance(user.email, (str, Email))
    assert len(user.name) > 0
    assert "@" in user.email


def test_user_factory_builds_batch() -> None:
    """Builds a batch of users; asserts count and that each has non-empty name and email."""
    users = UserFactory.batch(3)
    assert len(users) == 3
    for user in users:
        assert isinstance(user, User)
        assert len(user.name) > 0
        assert "@" in user.email


def test_seed_random_and_capper_seed_produce_same_value() -> None:
    """Builds with UserFactory.seed_random(42) and with capper.seed(42) yield the same name."""
    from capper import seed

    UserFactory.seed_random(42)
    user_after_seed_random = UserFactory.build()
    seed(42)
    user_after_capper_seed = UserFactory.build()
    assert user_after_seed_random.name == user_after_capper_seed.name


def test_model_factory_uses_capper_faker() -> None:
    """Asserts ModelFactory.__faker__ is capper's faker to document the shared instance."""
    from polyfactory.factories.pydantic_factory import ModelFactory

    import capper

    assert ModelFactory.__faker__ is capper.faker


def test_dataclass_factory_builds_with_capper_types() -> None:
    """Dataclass with Name/Email via DataclassFactory; asserts non-empty and valid email."""

    @dataclass
    class Person:
        name: Name
        email: Email

    class PersonFactory(DataclassFactory[Person]):
        pass

    person = PersonFactory.build()
    assert isinstance(person.name, (str, Name))
    assert isinstance(person.email, (str, Email))
    assert len(person.name) > 0
    assert "@" in person.email


def test_dataclass_factory_batch() -> None:
    """Builds a batch of dataclass instances; asserts count and non-empty name and email."""

    @dataclass
    class Person:
        name: Name
        email: Email

    class PersonFactory(DataclassFactory[Person]):
        pass

    people = PersonFactory.batch(2)
    assert len(people) == 2
    for person in people:
        assert isinstance(person, Person)
        assert len(person.name) > 0
        assert "@" in person.email


def test_capper_types_auto_registered_with_polyfactory() -> None:
    """Importing capper registers types so Polyfactory can build a model with PhoneNumber."""
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    from capper import PhoneNumber

    class Contact(BaseModel):
        phone: PhoneNumber

    class ContactFactory(ModelFactory[Contact]):
        pass

    contact = ContactFactory.build()
    assert isinstance(contact.phone, (str, PhoneNumber))
    assert len(contact.phone) > 0
