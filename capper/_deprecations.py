"""Internal helpers for deprecation warnings.

Use warn_deprecated() to emit consistent DeprecationWarning messages.
"""

from __future__ import annotations

from warnings import warn


def warn_deprecated(
    name: str,
    *,
    removal_version: str,
    alternative: str | None = None,
    stacklevel: int = 2,
) -> None:
    """Emit a standardized DeprecationWarning for a Capper API.

    Args:
        name: Fully qualified name of the deprecated API.
        removal_version: Target version where the API is expected to be removed.
        alternative: Optional string describing the preferred replacement.
        stacklevel: Passed through to warnings.warn to point at the caller.
    """
    message = f"{name} is deprecated and will be removed in {removal_version}."
    if alternative:
        message += f" Use {alternative} instead."
    warn(message, DeprecationWarning, stacklevel=stacklevel)
