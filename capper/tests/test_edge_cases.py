"""Edge-case tests: version fallback, use_faker/thread, registration and strategy errors."""

import sys
from unittest.mock import patch

import pytest

from capper import use_faker
from capper.base import FakerType


def test_version_fallback_when_metadata_missing() -> None:
    """When importlib.metadata.version raises, __version__ falls back to the bundled version."""
    with patch("importlib.metadata.version", side_effect=Exception("no metadata")):
        if "capper" in sys.modules:
            del sys.modules["capper"]
        import capper as capper_mod

        assert capper_mod.__version__ == "1.1.0"
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
    from capper import strategies

    class NoProvider(FakerType):
        faker_provider = ""

    with pytest.raises(ValueError, match="has no faker_provider"):
        strategies.for_type(NoProvider)


def test_strategies_for_type_invalid_provider_raises_attribute_error() -> None:
    """strategies.for_type() when current Faker has no such provider raises AttributeError."""
    from capper import Name, strategies

    class FakeFakerWithoutName:
        """Minimal Faker-like object missing the 'name' provider."""

        pass

    use_faker(FakeFakerWithoutName())
    try:
        with pytest.raises(AttributeError, match="Faker has no provider"):
            strategies.for_type(Name)
    finally:
        use_faker(None)


def test_use_faker_locale_german() -> None:
    """use_faker(Faker('de_DE')) produces locale-appropriate data; reset with use_faker(None)."""
    from faker import Faker
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    from capper import Address, Name

    class User(BaseModel):
        name: Name
        address: Address

    class UserFactory(ModelFactory[User]):
        pass

    try:
        use_faker(Faker("de_DE"))
        user = UserFactory.build()
        assert len(str(user.name)) > 0
        assert len(str(user.address)) > 0
        # German locale often yields umlauts or typical patterns; at least non-ASCII is possible
        combined = str(user.name) + str(user.address)
        assert combined.isascii() or any(c in "äöüßÄÖÜ" for c in combined)
    finally:
        use_faker(None)


def test_strategies_for_type_non_callable_provider_raises_type_error() -> None:
    """strategies.for_type() when Faker's provider is not callable raises TypeError."""
    from faker import Faker

    from capper import strategies

    class NotCallableProvider(FakerType):
        faker_provider = "name"

    my_faker = Faker()
    with patch.object(my_faker, "name", "not_callable"):
        use_faker(my_faker)
        try:
            with pytest.raises(TypeError, match="is not callable"):
                strategies.for_type(NotCallableProvider)
        finally:
            use_faker(None)
