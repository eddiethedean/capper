"""Tests for Hypothesis strategies (require capper[hypothesis])."""

import pytest

pytest.importorskip("hypothesis")

from hypothesis import given
from hypothesis import strategies as st

import capper
import capper.strategies  # noqa: F401 - register types with Hypothesis
from capper import Email, HexColor
from capper.registry import build_type_registry

_BUILTIN_TYPES = tuple(build_type_registry(capper).values())


@given(data=st.data())
def test_from_type_produces_wrapped_instance(data: st.DataObject) -> None:
    """st.from_type(T) yields non-empty instances of each registered FakerType."""
    type_class = data.draw(st.sampled_from(_BUILTIN_TYPES), label="type_class")
    value = data.draw(st.from_type(type_class), label="value")
    assert type(value) is type_class
    assert len(str(value)) > 0


@given(st.from_type(Email))
def test_from_type_email_contains_at(email: Email) -> None:
    """st.from_type(Email) yields strings containing '@'."""
    assert type(email) is Email
    assert "@" in email
    assert len(email) > 0


@given(capper.strategies.for_type(HexColor))
def test_for_type_hex_color_format(color: HexColor) -> None:
    """strategies.for_type(HexColor) respects faker_kwargs for hex format."""
    assert type(color) is HexColor
    assert color.startswith("#") and len(color) == 7
