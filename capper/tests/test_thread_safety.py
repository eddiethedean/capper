"""Tests for thread-safe per-thread Faker: use_faker() and seed() are isolated per thread."""

import threading

from capper import Name, seed, use_faker


def test_use_faker_per_thread_isolation() -> None:
    """Two threads each set use_faker() to a different locale; builds use that thread's Faker."""
    from faker import Faker
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    results: dict[str, str] = {}

    def thread_de() -> None:
        de = Faker("de_DE")
        de.seed_instance(0)
        use_faker(de)

        class User(BaseModel):
            name: Name

        class UserFactory(ModelFactory[User]):
            pass

        user = UserFactory.build()
        results["de"] = str(user.name)

    def thread_en() -> None:
        en = Faker("en_US")
        en.seed_instance(0)
        use_faker(en)

        class User(BaseModel):
            name: Name

        class UserFactory(ModelFactory[User]):
            pass

        user = UserFactory.build()
        results["en"] = str(user.name)

    t1 = threading.Thread(target=thread_de)
    t2 = threading.Thread(target=thread_en)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert "de" in results and "en" in results
    assert len(results["de"]) > 0 and len(results["en"]) > 0
    assert results["de"] != results["en"], "Each thread must use its own locale-specific Faker"


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
    assert results["42"] != results["99"], (
        "Different seeds must produce different values per thread"
    )
    seed(42)

    class User(BaseModel):
        name: Name

    class UserFactory(ModelFactory[User]):
        pass

    again = UserFactory.build().name
    assert again == results["42"]
