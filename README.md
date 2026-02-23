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

- **Person**: `Name`, `FirstName`, `LastName`, `Job`
- **Geo**: `Address`, `City`, `Country`
- **Internet**: `Email`, `URL`, `IP`, `UserName`
- **Commerce**: `Company`, `Product`, `Currency`, `Price`
- **Date/time**: `Date`, `DateTime`, `Time`
- **Text**: `Paragraph`, `Sentence`
- **Phone**: `PhoneNumber`, `CountryCallingCode`
- **Finance**: `CreditCardNumber`, `CreditCardExpiry`, `CreditCardProvider`

Import from the top level: `from capper import Name, Email, Address, ...`  
See [docs/FAKER_PROVIDERS.md](docs/FAKER_PROVIDERS.md) for the Faker provider used by each type.

**Optional kwargs:** Subclass `FakerType` and set `faker_kwargs` to pass arguments to the Faker provider (e.g. `faker_kwargs = {"nb_words": 10}` for `Sentence`).

**Custom types:** Subclass `FakerType`, set `faker_provider` to the Faker method name (e.g. `"company"`), and optionally `faker_kwargs`. The type auto-registers with Polyfactory when the class is defined.

## Compatibility

Capper targets **Faker >= 20.0** and **Polyfactory >= 2.0**. Major Faker upgrades may change or rename provider methods; if a type fails, check [Faker's changelog](https://faker.readthedocs.io/en/stable/changelog.html) and [docs/FAKER_PROVIDERS.md](docs/FAKER_PROVIDERS.md) and update the provider name if needed.

## Development

```bash
pip install -e ".[dev]"
pytest capper/tests
```

## Publishing

Releases are built and published to PyPI via [GitHub Actions](.github/workflows/publish.yml). To publish:

1. Add a `PYPI_API_TOKEN` secret (PyPI API token) to the repo.
2. Create a GitHub release (tag e.g. `v0.2.0`). The workflow runs tests, builds the package, and uploads to PyPI.

To build and upload manually: `pip install build twine`, `python -m build`, `twine upload dist/*`.

## Links

- [Package plan](capper_package_plan.md) — design and rationale
- [Roadmap](docs/ROADMAP.md) — development phases and status
- [Faker provider mapping](docs/FAKER_PROVIDERS.md) — type-to-provider reference
