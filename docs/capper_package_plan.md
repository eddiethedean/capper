# Capper: Polyfactory-First Semantic Faker Package

Design and rationale for the **capper** package. For install and usage see the main [README](README.md); for status and phases see the [Roadmap](ROADMAP.md).

## Package Name

`capper`

## Goal

Provide **semantic, typed wrappers for Faker providers** that automatically work with Polyfactory. Users just annotate fields with types — no extra steps required.

---

## 1. Core Principle

> Capper = Semantic Faker types + automatic Polyfactory integration

- Importing a type is enough: Polyfactory recognizes it and uses the correct Faker provider.
- Fully compatible with Pydantic, dataclasses, TypedDict, etc.

---

## 2. Package Layout

```
capper/
├── __init__.py            # imports all semantic types for direct use
├── base.py                # FakerType base class with automatic provider registration
├── person.py              # Name, FirstName, LastName, etc.
├── geo.py                 # Address, City, Country, etc.
├── internet.py            # Email, URL, IP, etc.
├── commerce.py            # Company, Product, Currency, Price
├── date_time.py           # Date, DateTime, Time
├── registry.py            # Auto-register all types with Polyfactory on import
├── tests/
│   ├── test_types.py
│   └── test_polyfactory_integration.py
└── examples/
    └── user_factory.py
```

---

## 3. Automatic Registration

```python
# base.py
from polyfactory.registry import register_provider
from faker import Faker

faker = Faker()

class FakerType:
    faker_provider: str  # subclass must define this

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        register_provider(cls, lambda *args, faker=faker, cls=cls, **kwargs: getattr(faker, cls.faker_provider)())
```

- Every subclass automatically registers with Polyfactory.
- No manual registration required.

---

## 4. Example Semantic Types

```python
# person.py
from .base import FakerType

class Name(FakerType):
    faker_provider = "name"

class FirstName(FakerType):
    faker_provider = "first_name"

class LastName(FakerType):
    faker_provider = "last_name"
```

---

## 5. Usage with Polyfactory

```python
from pydantic import BaseModel
from capper import Name, Email
from polyfactory.factories.pydantic_factory import ModelFactory

class User(BaseModel):
    name: Name
    email: Email

class UserFactory(ModelFactory[User]):
    pass

user = UserFactory.build()
print(user.name)
print(user.email)
```

Example output (varies each run): `Ashley Martin` / `hughesricardo@example.com`

✅ Works automatically. ✅ No extra steps. ✅ IDE autocompletion.

---

## 6. Advantages

- Zero friction — just import types.
- Strong typing & documentation.
- Future-proof: adding new types is simple.
- Works out-of-the-box with Pydantic models.

---

## 7. Development Plan

### Phase 1 — MVP

- Implement `FakerType` base class with automatic Polyfactory registration.
- Implement 15–20 core semantic types.
- Unit tests for Polyfactory integration.

### Phase 2 — Full Coverage

- Add remaining Faker providers (Commerce, Text, Date/Time, Phone, Credit cards).
- Ensure auto-registration on import.

### Phase 3 — Packaging

- `pyproject.toml` with `Faker` and `Polyfactory` dependencies.
- Publish to PyPI.
- Add usage examples.

### Phase 4 — Optional Enhancements

- Support Faker provider kwargs (min/max lengths, locales).
- Auto-sync with new Faker releases.

---

## 8. Dependencies

- **Required**: `Faker>=20.0`, `Polyfactory>=2.0`

---

## 9. Key Decisions

- Polyfactory is required.
- Semantic types are fully importable; no registration needed.
- Pydantic-compatible by default.
- Explicit type mapping only; no heuristics.

---

## 10. Future Enhancements

- Hypothesis strategies for property-based testing.
- Custom type registration by users.
- Syncing with new Faker providers.
- Optional CLI for generating example datasets.

---

This approach makes Capper a **plug-and-play semantic Faker layer for Polyfactory** — simple, clean, and developer-friendly.

---

*See also: [README](README.md) · [Roadmap](ROADMAP.md) · [Faker providers](FAKER_PROVIDERS.md)*

