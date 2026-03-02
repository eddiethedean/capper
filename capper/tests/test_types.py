"""Tests for capper types: Faker provider availability, ModelFactory registration, kwargs, seed."""

import pytest

from capper import (
    EAN8,
    EAN13,
    IP,
    URL,
    UUID,
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
    FileExtension,
    FileName,
    FilePath,
    FirstName,
    HexColor,
    Job,
    LastName,
    Name,
    Paragraph,
    PhoneNumber,
    Price,
    Product,
    Sentence,
    Time,
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
        FilePath,
        FileName,
        FileExtension,
        UUID,
        HexColor,
        EAN13,
        EAN8,
    ],
)
def test_type_generates_non_empty_string(type_class: type) -> None:
    """Each type's Faker provider exists and returns a non-empty value."""
    from faker import Faker

    faker = Faker()
    provider_name = getattr(type_class, "faker_provider")
    kwargs = getattr(type_class, "faker_kwargs", None) or {}
    value = getattr(faker, provider_name)(**kwargs)
    assert isinstance(value, (str, type_class))
    assert len(str(value)) > 0


@pytest.mark.parametrize(
    "type_class",
    [
        Name,
        Email,
        PhoneNumber,
        FirstName,
        Address,
        Sentence,
        CreditCardNumber,
        FilePath,
        UUID,
        HexColor,
        EAN13,
    ],
)
def test_model_factory_builds_capper_type(type_class: type) -> None:
    """Pydantic model with one capper type via ModelFactory; asserts non-empty and type."""
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
    """faker_kwargs passed to provider; ModelFactory builds and checks value."""
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


def test_hex_color_format() -> None:
    """HexColor yields a string starting with #."""
    from faker import Faker

    faker = Faker()
    value = faker.color(color_format="hex")
    assert isinstance(value, str) and value.startswith("#") and len(value) == 7


def test_seed_reproducibility(seeded_faker: None) -> None:
    """Builds twice after seeding with same value; asserts identical generated name."""
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    from capper import Name, seed

    class User(BaseModel):
        name: Name

    class UserFactory(ModelFactory[User]):
        pass

    seed(42)
    user1 = UserFactory.build()
    seed(42)
    user2 = UserFactory.build()
    assert user1.name == user2.name


def test_use_faker_switches_global_faker() -> None:
    """use_faker() sets this thread's Faker; next factory build uses that instance (e.g. seed)."""
    from faker import Faker
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    from capper import Name, use_faker

    try:
        custom = Faker()
        custom.seed_instance(123)
        use_faker(custom)

        class User(BaseModel):
            name: Name

        class UserFactory(ModelFactory[User]):
            pass

        seed_val = 999
        custom.seed_instance(seed_val)
        user1 = UserFactory.build()
        custom.seed_instance(seed_val)
        user2 = UserFactory.build()
        assert user1.name == user2.name
    finally:
        use_faker(None)
