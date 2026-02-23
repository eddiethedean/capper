"""Shared pytest fixtures for capper tests."""

import pytest


@pytest.fixture
def seeded_faker() -> None:
    """Seed the shared Faker (capper + Polyfactory) with 42 for reproducible test data."""
    from capper import seed

    seed(42)
