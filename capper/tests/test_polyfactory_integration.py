"""Tests for Polyfactory: ModelFactory, DataclassFactory, shared Faker, auto-registration."""

from dataclasses import dataclass

from polyfactory.factories import DataclassFactory
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

from capper import Email, Name, Sentence, faker_field, seed


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    pass


def test_user_factory_builds_with_capper_types() -> None:
    """Builds a User with Name and Email via ModelFactory; asserts non-empty and valid email."""
    user = UserFactory.build()
    assert type(user.name) is Name
    assert type(user.email) is Email
    assert len(user.name) > 0
    assert "@" in user.email


def test_user_factory_builds_batch() -> None:
    """Builds a batch of users; asserts count and that each has non-empty name and email."""
    users = UserFactory.batch(3)
    assert len(users) == 3
    for user in users:
        assert isinstance(user, User)
        assert type(user.name) is Name
        assert type(user.email) is Email
        assert len(user.name) > 0
        assert "@" in user.email


def test_seed_random_and_capper_seed_produce_same_value() -> None:
    """Builds with UserFactory.seed_random(42) and with capper.seed(42) yield the same values."""
    UserFactory.seed_random(42)
    user_after_seed_random = UserFactory.build()
    seed(42)
    user_after_capper_seed = UserFactory.build()
    assert user_after_seed_random.name == user_after_capper_seed.name
    assert user_after_seed_random.email == user_after_capper_seed.email


def test_model_factory_uses_capper_faker() -> None:
    """Asserts ModelFactory.__faker__ is capper's faker to document the shared instance."""
    from polyfactory.factories.pydantic_factory import ModelFactory

    import capper

    assert ModelFactory.__faker__ is capper.faker


def test_dataclass_factory_builds_with_capper_types() -> None:
    """Dataclass with Name/Email via DataclassFactory returns FakerType instances."""

    @dataclass
    class Person:
        name: Name
        email: Email

    class PersonFactory(DataclassFactory[Person]):
        pass

    person = PersonFactory.build()
    assert type(person.name) is Name
    assert type(person.email) is Email
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
        assert type(person.name) is Name
        assert type(person.email) is Email
        assert len(person.name) > 0
        assert "@" in person.email


def test_faker_field_override_with_provider_kwargs() -> None:
    """Polyfactory-style field override: faker_field(Sentence, nb_words=n) uses provider kwargs."""

    class Post(BaseModel):
        summary: Sentence
        body: Sentence

    class PostFactory(ModelFactory[Post]):
        summary = faker_field(Sentence, nb_words=5)
        body = faker_field(Sentence, nb_words=12)

    post = PostFactory.build()
    assert type(post.summary) is Sentence
    assert type(post.body) is Sentence
    assert len(post.summary) > 0 and len(post.summary.split()) >= 1
    assert len(post.body) > 0 and len(post.body.split()) >= 1

    seed(0)
    short = faker_field(Sentence, nb_words=5)()
    seed(0)
    long = faker_field(Sentence, nb_words=12)()
    assert short != long


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
    assert type(contact.phone) is PhoneNumber
    assert len(contact.phone) > 0


def test_pydantic_coerces_str_to_faker_type() -> None:
    """model_validate coerces plain strings to FakerType subclasses."""
    user = User.model_validate({"name": "Ada Lovelace", "email": "ada@example.com"})
    assert type(user.name) is Name
    assert type(user.email) is Email
    assert user.name == "Ada Lovelace"
    assert user.email == "ada@example.com"


def test_pydantic_rejects_invalid_faker_type_input() -> None:
    """model_validate rejects non-string values for FakerType fields."""
    import pytest

    with pytest.raises(Exception):
        User.model_validate({"name": 123, "email": "ada@example.com"})
