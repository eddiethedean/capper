# Capper

Semantic, typed wrappers for [Faker](https://faker.readthedocs.io/) with automatic [Polyfactory](https://polyfactory.litestar.dev/) integration.

## Goal

Use **semantic types** (e.g. `Name`, `Email`) in your models — Polyfactory picks the right Faker provider automatically. No manual registration. Works with **Pydantic**, **dataclasses**, **attrs**, and other Polyfactory-supported models.

## Install

```bash
pip install capper
```

Requires **Python 3.9+**, **Faker >= 20.0**, and **Polyfactory >= 2.0**. For **Pydantic** models, install the optional extra:

```bash
pip install capper[pydantic]
```

## Usage

**With Pydantic** (requires `capper[pydantic]`):

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

**With dataclasses** (no Pydantic needed):

```python
from dataclasses import dataclass
from capper import Name, Email
from polyfactory.factories import DataclassFactory

@dataclass
class User:
    name: Name
    email: Email

class UserFactory(DataclassFactory[User]):
    pass

user = UserFactory.build()
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
