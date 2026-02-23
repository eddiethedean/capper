# Capper

Semantic, typed wrappers for [Faker](https://faker.readthedocs.io/) with automatic [Polyfactory](https://polyfactory.litestar.dev/) integration.

## Goal

Use **semantic types** (e.g. `Name`, `Email`) in your Pydantic models — Polyfactory picks the right Faker provider automatically. No manual registration.

## Install

```bash
pip install capper
```

Requires **Python 3.9+**, **Faker >= 20.0**, **Polyfactory >= 2.0**, and **Pydantic >= 2.0**.

## Usage

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
print(user.name)   # e.g., "Ashley Johnson"
print(user.email)  # e.g., "ashley.johnson@example.com"
```

Works automatically. No extra steps. IDE autocompletion.

## Available types

- **Person**: `Name`, `FirstName`, `LastName`
- **Geo**: `Address`, `City`, `Country`
- **Internet**: `Email`, `URL`, `IP`
- **Commerce**: `Company`, `Product`, `Currency`, `Price`
- **Date/time**: `Date`, `DateTime`, `Time`

Import from the top level: `from capper import Name, Email, Address, ...`

## Development

```bash
pip install -e ".[dev]"
pytest capper/tests
```

## Links

- [Package plan](capper_package_plan.md) — design and rationale
- [Roadmap](docs/ROADMAP.md) — development phases and status
