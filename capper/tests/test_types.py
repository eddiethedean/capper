"""Tests for capper types: ModelFactory registration, kwargs, seed, and HexColor."""

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

ALL_CAPPER_TYPES = [
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
]


@pytest.mark.parametrize("type_class", ALL_CAPPER_TYPES)
def test_model_factory_builds_capper_type(type_class: type) -> None:
    """ModelFactory builds each capper type as a wrapped FakerType with a non-empty value."""
    from typing import Any, Type

    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import create_model

    model_cls: Type[Any] = create_model("Model", value=(type_class, ...))

    class ModelFactoryCls(ModelFactory[model_cls]):  # type: ignore[valid-type]
        pass

    instance: Any = ModelFactoryCls.build()
    assert type(instance.value) is type_class
    assert len(str(instance.value)) > 0


def test_hex_color_via_model_factory() -> None:
    """HexColor uses faker_kwargs to produce a #RRGGBB string through capper registration."""
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import create_model

    model_cls = create_model("HexColorModel", color=(HexColor, ...))

    class HexColorFactory(ModelFactory[model_cls]):  # type: ignore[valid-type]
        pass

    value = HexColorFactory.build().color
    assert type(value) is HexColor
    assert value.startswith("#") and len(value) == 7


def test_faker_kwargs_support() -> None:
    """faker_kwargs passed to provider; ModelFactory builds wrapped ShortSentence values."""
    from faker import Faker
    from polyfactory.factories.pydantic_factory import ModelFactory as PFModelFactory
    from pydantic import BaseModel

    from capper import seed
    from capper.base import FakerType

    class ShortSentence(FakerType):
        faker_provider = "sentence"
        faker_kwargs = {"nb_words": 5}

    faker = Faker()
    expected = faker.sentence(nb_words=5)
    assert isinstance(expected, str) and len(expected) > 0

    class FakerKwargsModel(BaseModel):
        text: ShortSentence

    class FakerKwargsModelFactory(PFModelFactory[FakerKwargsModel]):
        pass

    seed(123)
    instance = FakerKwargsModelFactory.build()
    assert type(instance.text) is ShortSentence
    assert len(instance.text) > 0


def test_seed_reproducibility() -> None:
    """Builds twice after seeding with same value; asserts identical generated name."""
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    from capper import seed

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

    from capper import use_faker

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
