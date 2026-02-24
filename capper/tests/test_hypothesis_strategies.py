"""Tests for Hypothesis strategies (require capper[hypothesis])."""

import pytest

pytest.importorskip("hypothesis")

from hypothesis import given
from hypothesis import strategies as st

import capper.strategies  # noqa: F401 - register types with Hypothesis
from capper import Email, Name


@given(st.from_type(Name))
def test_from_type_name_produces_non_empty_string(name: Name) -> None:
    """st.from_type(Name) yields non-empty Name instances."""
    assert isinstance(name, Name)
    assert isinstance(name, str)
    assert len(name) > 0


@given(st.from_type(Email))
def test_from_type_email_contains_at(email: Email) -> None:
    """st.from_type(Email) yields strings containing '@'."""
    assert isinstance(email, Email)
    assert "@" in email
    assert len(email) > 0


@given(capper.strategies.for_type(Name))
def test_for_type_name_produces_name(name: Name) -> None:
    """strategies.for_type(Name) yields Name instances."""
    assert isinstance(name, Name)
    assert len(name) > 0
