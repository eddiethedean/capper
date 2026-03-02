"""Tests for build_type_registry behavior."""

from __future__ import annotations

from types import SimpleNamespace

from capper.base import FakerType
from capper.registry import build_type_registry


def test_build_type_registry_includes_only_fakertype_with_provider() -> None:
    """Only FakerType subclasses with non-empty faker_provider from __all__ are included."""

    class GoodType(FakerType):
        faker_provider = "name"

    class NoProvider(FakerType):
        faker_provider = ""

    class NotAFakerType:
        faker_provider = "name"

    class AlsoGood(FakerType):
        faker_provider = "email"

    module = SimpleNamespace(
        __all__=["GoodType", "NoProvider", "NotAFakerType", "AlsoGood"],
        GoodType=GoodType,
        NoProvider=NoProvider,
        NotAFakerType=NotAFakerType,
        AlsoGood=AlsoGood,
    )

    registry = build_type_registry(module)  # type: ignore[arg-type]

    assert set(registry.keys()) == {"GoodType", "AlsoGood"}
    assert registry["GoodType"] is GoodType
    assert registry["AlsoGood"] is AlsoGood


def test_build_type_registry_ignores_names_not_in_all() -> None:
    """Attributes not listed in __all__ are ignored."""

    class HiddenType(FakerType):
        faker_provider = "name"

    module = SimpleNamespace(__all__=[], HiddenType=HiddenType)

    registry = build_type_registry(module)  # type: ignore[arg-type]
    assert registry == {}
