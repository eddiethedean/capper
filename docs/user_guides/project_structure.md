## Project structure patterns with Capper

As your project grows, it helps to keep Capper types and factories organized.
This guide suggests a simple layout and naming patterns that work for most codebases.

### Suggested layout

For an application package `myapp`:

```text
myapp/
    __init__.py
    types.py           # Capper-backed types specific to your domain
    factories.py       # Polyfactory factories for your models/schemas
    api_schemas.py     # Pydantic models for API payloads
    services.py        # Business logic
tests/
    conftest.py        # shared fixtures, seeding, Hypothesis setup
    test_api.py
    test_services.py
```

Keep Capper-focused code (`types.py`, `factories.py`) close to where it is used, and keep test-specific wiring in `tests/`.

### Types module

Put shared Capper types in one place and re-export them from your package:

```python
# myapp/types.py
from capper import FakerType


class AccountId(FakerType):
    faker_provider = "uuid4"


class OrderNumber(FakerType):
    faker_provider = "ean13"
```

Then re-export from `myapp/__init__.py` if you want:

```python
from .types import AccountId, OrderNumber

__all__ = ["AccountId", "OrderNumber"]
```

### Factories module

Centralize Polyfactory factories:

```python
# myapp/factories.py
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory

from .types import AccountId


class Account(BaseModel):
    id: AccountId
    email: str


class AccountFactory(ModelFactory[Account]):
    __random_seed__ = 123
```

Tests import factories, not Capper directly:

```python
from myapp.factories import AccountFactory


def test_account_email_is_string() -> None:
    account = AccountFactory.build()
    assert isinstance(account.email, str)
```

### When to create a separate “type pack”

Create a separate package (a **type pack**) when:

- The types are useful across multiple projects or teams.
- You want to version and publish them independently of a single app.

See [Extending Capper](../extending.md) for a detailed example of a type pack.

### Thread-safety and seeding reminders

- Capper uses a per-thread Faker instance via a proxy.
- Call `seed(n)` or set `__random_seed__` on factories **inside the thread** where tests run.
- For locale-specific data, use `use_faker(Faker("de_DE"))` to keep Capper and Polyfactory in sync.

See also:

- [Reproducible data](reproducible_data.md)
- [Extending Capper](../extending.md)
