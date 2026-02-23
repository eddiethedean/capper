"""Tests that capper types generate valid values via Faker."""

import pytest

from capper import (
    Address,
    City,
    Company,
    Country,
    Currency,
    Date,
    DateTime,
    Email,
    FirstName,
    IP,
    LastName,
    Name,
    Price,
    Product,
    Time,
    URL,
)


@pytest.mark.parametrize(
    "type_class",
    [
        Name,
        FirstName,
        LastName,
        Address,
        City,
        Country,
        Email,
        URL,
        IP,
        Company,
        Product,
        Currency,
        Price,
        Date,
        DateTime,
        Time,
    ],
)
def test_type_generates_non_empty_string(type_class: type) -> None:
    """Each semantic type produces a non-empty string when used as a provider."""
    from faker import Faker

    faker = Faker()
    provider_name = type_class.faker_provider
    value = getattr(faker, provider_name)()
    assert isinstance(value, (str, type_class))
    assert len(str(value)) > 0
