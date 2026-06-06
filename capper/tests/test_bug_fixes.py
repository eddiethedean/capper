"""Regression tests for bug-audit fixes."""

import sys

import pytest

if sys.version_info >= (3, 10):
    from capper import cli
else:
    cli = None  # type: ignore[assignment]


def test_faker_field_uses_thread_faker_after_use_faker_reset() -> None:
    """faker_field resolves the provider at call time, not at creation time."""
    from faker import Faker

    from capper import Sentence, faker, faker_field, seed, use_faker

    use_faker(Faker("fr_FR"))
    gen = faker_field(Sentence, nb_words=2)
    use_faker(None)

    seed(1)
    result = gen()
    seed(1)
    expected = faker.sentence(nb_words=2)
    assert str(result) == str(expected)


def test_dataclass_factory_returns_faker_type_instances() -> None:
    """Polyfactory providers return FakerType instances, not plain str."""
    from dataclasses import dataclass

    from polyfactory.factories import DataclassFactory

    from capper import Email, Name

    @dataclass
    class Person:
        name: Name
        email: Email

    class PersonFactory(DataclassFactory[Person]):
        pass

    person = PersonFactory.build()
    assert type(person.name) is Name
    assert type(person.email) is Email


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
def test_cli_address_produces_one_line_per_row(capsys: pytest.CaptureFixture[str]) -> None:
    """CLI escapes embedded newlines so each logical row is one physical line."""
    orig_argv = sys.argv
    try:
        sys.argv = ["capper", "generate", "Name", "Address", "--count", "3", "--seed", "1"]
        assert cli.main() == 0
        out = capsys.readouterr().out
        lines = out.strip().splitlines()
        assert len(lines) == 3
        for line in lines:
            parts = line.split("\t")
            assert len(parts) == 2
            assert "\\n" in parts[1] or "\n" not in parts[1]
    finally:
        sys.argv = orig_argv


def test_hypothesis_draw_does_not_pollute_capper_seed() -> None:
    """Hypothesis for_type uses an isolated Faker and does not advance the thread-local sequence."""
    pytest.importorskip("hypothesis")
    from hypothesis import strategies as st
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    import capper.strategies  # noqa: F401
    from capper import Name, seed

    class User(BaseModel):
        name: Name

    class UserFactory(ModelFactory[User]):
        pass

    seed(42)
    baseline = UserFactory.build().name
    st.from_type(Name).example()
    seed(42)
    after_hyp = UserFactory.build().name
    assert after_hyp == baseline


def test_seed_rejects_non_int() -> None:
    """seed() requires an integer argument."""
    from capper import seed

    with pytest.raises(TypeError, match="requires an int"):
        seed("42")  # type: ignore[arg-type]


def test_use_faker_rejects_non_faker_instance() -> None:
    """use_faker() rejects objects that are not Faker instances."""
    from capper import use_faker

    with pytest.raises(TypeError, match="requires a Faker instance"):
        use_faker(object())  # type: ignore[arg-type]


def test_faker_type_rejects_empty_provider() -> None:
    """Empty faker_provider fails at class definition with ValueError."""
    from capper.base import FakerType

    with pytest.raises(ValueError, match="has no faker_provider"):

        class Empty(FakerType):
            faker_provider = ""


def test_faker_type_nominal_pydantic_accepts_unvalidated_strings() -> None:
    """FakerType Pydantic fields are nominal: format is not validated on manual input."""
    from pydantic import BaseModel

    from capper import Email, Name

    class User(BaseModel):
        name: Name
        email: Email

    user = User.model_validate({"name": "", "email": "not-an-email"})
    assert type(user.name) is Name
    assert type(user.email) is Email
    assert user.email == "not-an-email"


def test_faker_type_rejects_non_string_provider() -> None:
    """Non-string faker_provider fails at class definition with a clear error."""
    from capper.base import FakerType

    with pytest.raises(TypeError, match="faker_provider must be a non-empty str"):

        class Bad(FakerType):
            faker_provider = 123  # type: ignore[assignment]


def test_faker_proxy_is_not_faker_instance() -> None:
    """capper.faker is a thread-local proxy, not a concrete Faker instance."""
    from faker import Faker

    import capper

    assert not isinstance(capper.faker, Faker)
    assert capper.faker.name()  # delegated to thread-local Faker


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
def test_cli_max_count_exits_nonzero(capsys: pytest.CaptureFixture[str]) -> None:
    """CLI rejects --count above the maximum allowed rows."""
    orig_argv = sys.argv
    try:
        sys.argv = ["capper", "generate", "Name", "--count", str(cli.MAX_GENERATE_COUNT + 1)]
        assert cli.main() == 1
        assert "maximum is" in capsys.readouterr().err
    finally:
        sys.argv = orig_argv


def test_faker_field_empty_provider_raises_attribute_error() -> None:
    """faker_field() rejects types with an empty faker_provider attribute."""

    class EmptyProvider:
        faker_provider = ""

    from capper.fields import faker_field

    with pytest.raises(AttributeError, match="has no faker_provider"):
        faker_field(EmptyProvider)  # type: ignore[arg-type]


def test_register_duplicate_provider_emits_warning() -> None:
    """Re-registering the same FakerType with Polyfactory emits a warning."""
    import warnings

    from capper import Name
    from capper.base import _register

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        _register(Name, "name")
    assert caught
    assert "Re-registering" in str(caught[0].message)


def test_register_rejects_empty_provider_name() -> None:
    """_register() rejects an empty provider name."""
    from capper import Name
    from capper.base import _register

    with pytest.raises(ValueError, match="has no faker_provider"):
        _register(Name, "")


def test_strategies_for_type_rejects_non_string_provider() -> None:
    """strategies.for_type() rejects non-string faker_provider values."""
    from capper import strategies

    class BadProvider:
        faker_provider = 123  # type: ignore[assignment]

    with pytest.raises(TypeError, match="faker_provider must be a non-empty str"):
        strategies.for_type(BadProvider)  # type: ignore[arg-type]
    """CLI copies faker_kwargs so in-place edits to the per-call dict do not mutate the class."""
    from capper import HexColor

    original = dict(HexColor.faker_kwargs)
    kwargs = dict(HexColor.faker_kwargs)
    kwargs["color_format"] = "rgb"
    assert HexColor.faker_kwargs == original
