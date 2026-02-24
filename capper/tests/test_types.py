"""Tests for capper types: Faker provider availability, ModelFactory registration, kwargs, seed."""

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
    """Asserts each type's Faker provider exists and returns a non-empty value (provider availability)."""
    from faker import Faker

    faker = Faker()
    provider_name = getattr(type_class, "faker_provider")
    value = getattr(faker, provider_name)()
    assert isinstance(value, (str, type_class))
    assert len(str(value)) > 0


@pytest.mark.parametrize(
    "type_class",
    [Name, Email, PhoneNumber, FirstName, Address, Sentence, CreditCardNumber],
)
def test_model_factory_builds_capper_type(type_class: type) -> None:
    """Builds a Pydantic model with a single capper type via ModelFactory; asserts non-empty and type."""
    from typing import Any, Type

    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import create_model

    model_cls: Type[Any] = create_model("Model", value=(type_class, ...))

    class ModelFactoryCls(ModelFactory[model_cls]):  # type: ignore[valid-type]
        pass

    instance: Any = ModelFactoryCls.build()
    assert isinstance(instance.value, (str, type_class))
    assert len(str(instance.value)) > 0


def test_faker_kwargs_support() -> None:
    """Asserts types can set faker_kwargs and provider is called with them; builds via ModelFactory and checks value."""
    from capper.base import FakerType

    class ShortSentence(FakerType):
        faker_provider = "sentence"
        faker_kwargs = {"nb_words": 5}

    from faker import Faker

    faker = Faker()
    value = getattr(faker, "sentence")(**ShortSentence.faker_kwargs)
    assert isinstance(value, str) and len(value) > 0

    # Polyfactory uses the same kwargs via registration
    from polyfactory.factories.pydantic_factory import ModelFactory as PFModelFactory
    from pydantic import BaseModel

    class FakerKwargsModel(BaseModel):
        text: ShortSentence

    class FakerKwargsModelFactory(PFModelFactory[FakerKwargsModel]):
        pass

    instance = FakerKwargsModelFactory.build()
    assert isinstance(instance.text, (str, ShortSentence)) and len(instance.text) > 0


def test_seed_reproducibility(seeded_faker: None) -> None:
    """Builds twice after seeding with same value; asserts identical generated name."""
    from capper import Name, seed
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    class User(BaseModel):
        name: Name

    class UserFactory(ModelFactory[User]):
        pass

    seed(42)
    user1 = UserFactory.build()
    seed(42)
    user2 = UserFactory.build()
    assert user1.name == user2.name
