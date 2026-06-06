"""Tests for the internal deprecation helper."""

from __future__ import annotations

from warnings import catch_warnings, simplefilter

from capper._deprecations import warn_deprecated


def test_warn_deprecated_emits_standard_message() -> None:
    """warn_deprecated() emits a DeprecationWarning with the expected text."""
    with catch_warnings(record=True) as caught:
        simplefilter("always", DeprecationWarning)
        warn_deprecated(
            "capper.some_api",
            removal_version="0.6.0",
            alternative="capper.new_api",
            stacklevel=1,
        )

    assert caught, "Expected at least one DeprecationWarning"
    warning = caught[0]
    assert issubclass(warning.category, DeprecationWarning)
    message = str(warning.message)
    assert "capper.some_api is deprecated and will be removed in 0.6.0." in message
    assert "Use capper.new_api instead." in message


def test_warn_deprecated_without_alternative() -> None:
    """warn_deprecated() omits the alternative line when none is provided."""
    with catch_warnings(record=True) as caught:
        simplefilter("always", DeprecationWarning)
        warn_deprecated("capper.old_api", removal_version="2.0.0", stacklevel=1)

    assert caught
    message = str(caught[0].message)
    assert "capper.old_api is deprecated and will be removed in 2.0.0." in message
    assert "instead." not in message
