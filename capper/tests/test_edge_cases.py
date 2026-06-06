"""Edge-case tests: version fallback, use_faker/thread, registration and strategy errors."""

import sys
from unittest.mock import patch

import pytest

from capper import use_faker
from capper.base import FakerType


def test_version_fallback_when_metadata_missing() -> None:
    """When importlib.metadata.version raises PackageNotFoundError, __version__ falls back."""
    from importlib.metadata import PackageNotFoundError

    with patch("importlib.metadata.version", side_effect=PackageNotFoundError("capper")):
        if "capper" in sys.modules:
            del sys.modules["capper"]
        import capper as capper_mod

        assert capper_mod.__version__ == "1.1.1"
    # Reimport so later tests see the real version
    if "capper" in sys.modules:
        del sys.modules["capper"]
    import capper  # noqa: F401


def test_use_faker_none_in_fresh_thread_covers_attribute_error() -> None:
    """use_faker(None) in a thread that never set faker hits the except AttributeError path."""
    result: list[Exception | None] = []

    def run_in_thread() -> None:
        try:
            use_faker(None)
            result.append(None)
        except Exception as e:
            result.append(e)

    import threading

    t = threading.Thread(target=run_in_thread)
    t.start()
    t.join()
    assert result == [None]


def test_register_invalid_provider_raises_attribute_error() -> None:
    """Defining a FakerType subclass with nonexistent faker_provider raises AttributeError."""
    with pytest.raises(AttributeError, match="Faker has no provider .nonexistent_xyz."):

        class BadType(FakerType):
            faker_provider = "nonexistent_xyz"


def test_register_non_callable_provider_raises_type_error() -> None:
    """When Faker has the provider name but it is not callable, _register raises TypeError."""
    from faker import Faker

    my_faker = Faker()
    with patch.object(my_faker, "name", "not_callable"):
        use_faker(my_faker)
        try:
            with pytest.raises(TypeError, match="is not callable"):

                class BadCallableType(FakerType):
                    faker_provider = "name"

        finally:
            use_faker(None)


def test_strategies_for_type_no_provider_raises_value_error() -> None:
    """strategies.for_type() on a class with no faker_provider raises ValueError."""

    class NoProvider:
        """Stand-in type without faker_provider (cannot subclass FakerType with empty provider)."""

        __name__ = "NoProvider"

    from capper import strategies

    with pytest.raises(ValueError, match="has no faker_provider"):
        strategies.for_type(NoProvider)  # type: ignore[arg-type]


def test_strategies_for_type_invalid_provider_raises_attribute_error() -> None:
    """strategies.for_type() with an unknown provider name raises AttributeError."""
    from capper import strategies

    class BadProvider:
        faker_provider = "nonexistent_xyz_for_strategies"

    with pytest.raises(AttributeError, match="Faker has no provider"):
        strategies.for_type(BadProvider)  # type: ignore[arg-type]


def test_use_faker_locale_german() -> None:
    """use_faker(Faker('de_DE')) routes generation through the German locale Faker."""
    from faker import Faker
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    from capper import Name

    class User(BaseModel):
        name: Name

    class UserFactory(ModelFactory[User]):
        pass

    de = Faker("de_DE")
    en = Faker("en_US")
    try:
        de.seed_instance(0)
        use_faker(de)
        via_capper = UserFactory.build()

        de.seed_instance(0)
        use_faker(de)
        direct_de = de.name()

        en.seed_instance(0)
        direct_en = en.name()

        assert str(via_capper.name) == direct_de
        assert direct_de != direct_en
    finally:
        use_faker(None)


def test_use_faker_proxy_resets_thread_local() -> None:
    """Passing the capper faker proxy to use_faker() clears thread-local state."""
    from faker import Faker

    import capper

    custom = Faker("de_DE")
    custom.seed_instance(0)
    use_faker(custom)
    try:
        use_faker(capper.faker)
        default = capper.faker.name()
        assert isinstance(default, str) and len(default) > 0
    finally:
        use_faker(None)


def test_faker_field_invalid_provider_raises_attribute_error() -> None:
    """faker_field() raises when the provider is missing at generation time."""

    class MissingName:
        faker_provider = "nonexistent_xyz_for_faker_field"

    from capper.fields import faker_field

    gen = faker_field(MissingName)  # type: ignore[arg-type]
    with pytest.raises(AttributeError, match="Faker has no provider"):
        gen()


def test_faker_field_non_callable_provider_raises_type_error() -> None:
    """faker_field() raises when the provider is not callable at generation time."""
    from unittest.mock import MagicMock, patch

    from capper import Sentence, fields
    from capper.fields import faker_field

    gen = faker_field(Sentence)
    mock_faker = MagicMock()
    mock_faker.sentence = "not_callable"
    with patch.object(fields, "faker", mock_faker):
        with pytest.raises(TypeError, match="is not callable"):
            gen()


def test_faker_field_no_provider_raises_at_class_definition() -> None:
    """FakerType subclasses with empty faker_provider fail at class definition."""
    with pytest.raises(ValueError, match="has no faker_provider"):

        class NoProvider(FakerType):
            faker_provider = ""


def test_strategies_for_type_non_callable_provider_raises_type_error() -> None:
    """strategies.for_type() raises when the provider exists but is not callable."""
    from unittest.mock import patch

    from faker import Faker

    from capper import strategies

    class NameType(FakerType):
        faker_provider = "name"

    probe = Faker()
    with patch.object(probe, "name", "not_callable"):
        with patch.object(strategies, "Faker", return_value=probe):
            with pytest.raises(TypeError, match="is not callable"):
                strategies.for_type(NameType)
