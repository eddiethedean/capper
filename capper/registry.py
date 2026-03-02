from __future__ import annotations

from types import ModuleType
from typing import Dict, Type

from .base import FakerType


def build_type_registry(module: ModuleType) -> dict[str, Type[FakerType]]:
    """Return a mapping of public name -> FakerType subclass for the given module.

    Only names exported via ``module.__all__`` and backed by FakerType subclasses
    with a non-empty ``faker_provider`` are included.
    """
    registry: Dict[str, Type[FakerType]] = {}
    for name in getattr(module, "__all__", []):
        obj = getattr(module, name, None)
        provider = getattr(obj, "faker_provider", None)
        if (
            isinstance(obj, type)
            and issubclass(obj, FakerType)
            and isinstance(provider, str)
            and len(provider) > 0
        ):
            registry[name] = obj
    return registry
