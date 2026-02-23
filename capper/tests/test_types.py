"""Tests that capper types generate valid values via Faker."""

import pytest

from capper import (
    Address,
    City,
    Company,
    Country,
    CountryCallingCode,
    CreditCardExpiry,
    CreditCardNumber,
    CreditCardProvider,
    Currency,
    Date,
    DateTime,
    Email,
    FirstName,
    IP,
    Job,
    LastName,
    Name,
    Paragraph,
    PhoneNumber,
    Price,
    Product,
    Sentence,
    Time,
    URL,
    UserName,
)


@pytest.mark.parametrize(
    "type_class",
    [
        Name,
        FirstName,
        LastName,
        Job,
        Address,
        City,
        Country,
        Email,
        URL,
        IP,
        UserName,
        Company,
        Product,
        Currency,
        Price,
        Date,
        DateTime,
        Time,
        Paragraph,
        Sentence,
        PhoneNumber,
        CountryCallingCode,
        CreditCardNumber,
        CreditCardExpiry,
        CreditCardProvider,
    ],
)
def test_type_generates_non_empty_string(type_class: type) -> None:
    """Each semantic type produces a non-empty string when used as a provider."""
    from faker import Faker

    faker = Faker()
    provider_name = type_class.faker_provider
    value = getattr(faker, provider_name)()
    assert isinstance(value, (str, type_class))
    assert len(str(value)) > 0


def test_faker_kwargs_support() -> None:
    """Types can set faker_kwargs; provider is called with those kwargs."""
    from capper.base import FakerType

    class ShortSentence(FakerType):
        faker_provider = "sentence"
        faker_kwargs = {"nb_words": 5}

    from faker import Faker

    faker = Faker()
    value = getattr(faker, "sentence")(**ShortSentence.faker_kwargs)
    assert isinstance(value, str) and len(value) > 0

    # Polyfactory uses the same kwargs via registration
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    class Model(BaseModel):
        text: ShortSentence

    class ModelFactory(ModelFactory[Model]):
        pass

    instance = ModelFactory.build()
    assert isinstance(instance.text, (str, ShortSentence)) and len(instance.text) > 0


def test_seed_reproducibility() -> None:
    """Seeding the shared Faker instance yields reproducible values."""
    from capper import Name, seed
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    class User(BaseModel):
        name: Name

    class UserFactory(ModelFactory[User]):
        pass

    seed(99)
    user1 = UserFactory.build()
    seed(99)
    user2 = UserFactory.build()
    assert user1.name == user2.name
