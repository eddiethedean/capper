"""Tests for thread-safe per-thread Faker: use_faker() and seed() are isolated per thread."""

import threading

from capper import Name, seed, use_faker
from capper.base import _get_faker


def test_use_faker_per_thread_isolation() -> None:
    """Two threads each set use_faker() to a different locale; builds use that thread's Faker."""
    from faker import Faker
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    results: dict[str, str] = {}

    def thread_de() -> None:
        use_faker(Faker("de_DE"))
        assert _get_faker() is not None

        # Build a model; German locale often produces umlauts in names
        class User(BaseModel):
            name: Name

        class UserFactory(ModelFactory[User]):
            pass

        user = UserFactory.build()
        results["de"] = user.name

    def thread_en() -> None:
        use_faker(Faker("en_US"))
        assert _get_faker() is not None

        class User(BaseModel):
            name: Name

        class UserFactory(ModelFactory[User]):
            pass

        user = UserFactory.build()
        results["en"] = user.name

    t1 = threading.Thread(target=thread_de)
    t2 = threading.Thread(target=thread_en)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert "de" in results and "en" in results
    assert len(results["de"]) > 0 and len(results["en"]) > 0


def test_seed_per_thread_isolation() -> None:
    """seed(n) in one thread does not affect another thread's sequence."""
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    results: dict[str, str] = {}

    def thread_seed_42() -> None:
        seed(42)

        class User(BaseModel):
            name: Name

        class UserFactory(ModelFactory[User]):
            pass

        results["42"] = UserFactory.build().name

    def thread_seed_99() -> None:
        seed(99)

        class User(BaseModel):
            name: Name

        class UserFactory(ModelFactory[User]):
            pass

        results["99"] = UserFactory.build().name

    t1 = threading.Thread(target=thread_seed_42)
    t2 = threading.Thread(target=thread_seed_99)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert "42" in results and "99" in results
    # Same seed in same thread gives same result when run again
    seed(42)

    class User(BaseModel):
        name: Name

    class UserFactory(ModelFactory[User]):
        pass

    again = UserFactory.build().name
    assert again == results["42"]
