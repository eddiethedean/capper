"""Tests for faker_field helper: kwargs merging, seeding, and type behavior."""

from __future__ import annotations

from capper import Sentence, faker, faker_field, seed
from capper.base import FakerType


def test_faker_field_merges_type_faker_kwargs_and_overrides() -> None:
    """faker_field respects class-level faker_kwargs and allows per-field overrides."""

    class ShortSentence(FakerType):
        faker_provider = "sentence"
        faker_kwargs = {"nb_words": 2}

    base_gen = faker_field(ShortSentence)
    override_gen = faker_field(ShortSentence, nb_words=5)

    # With the same seed, the helper should mirror direct Faker provider calls.
    seed(123)
    expected_base = faker.sentence(nb_words=2)
    seed(123)
    value_base = base_gen()
    assert value_base == ShortSentence(expected_base)

    seed(456)
    expected_override = faker.sentence(nb_words=5)
    seed(456)
    value_override = override_gen()
    assert value_override == ShortSentence(expected_override)


def test_faker_field_respects_capper_seed_for_reproducibility() -> None:
    """Repeated seeding with the same value yields the same generated Sentence."""
    gen = faker_field(Sentence, nb_words=5)

    seed(999)
    first = gen()
    seed(999)
    second = gen()

    assert isinstance(first, Sentence)
    assert isinstance(second, Sentence)
    assert first == second
