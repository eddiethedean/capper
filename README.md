# Capper

Semantic, typed wrappers for [Faker](https://faker.readthedocs.io/) with automatic [Polyfactory](https://polyfactory.litestar.dev/) integration.

**Source:** [github.com/eddiethedean/capper](https://github.com/eddiethedean/capper)

## Why Capper?

- **Zero config** — Import a type; Polyfactory uses the right Faker provider. No manual registration.
- **Typed** — Use `Name`, `Email`, `PhoneNumber`, etc. in your models for clear intent and IDE support.
- **Multi-backend** — Works with Pydantic, dataclasses, attrs, and other [Polyfactory-supported](https://polyfactory.litestar.dev/) model types.
- **Optional Pydantic** — Install `capper` alone for dataclasses/attrs; add `capper[pydantic]` when you use Pydantic models.

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
print(user.name)
print(user.email)
```

Example output (varies each run):

```
Paul Blair
linda00@example.net
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
print(user.name)
print(user.email)
```

Example output (varies each run):

```
Carly Jenkins
oevans@example.com
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

**Reproducibility:** Capper and Polyfactory share the same Faker instance, so one seed controls both capper types and built-in types (`str`, `int`, etc.):

```python
from capper import seed, Name
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

class User(BaseModel):
    name: Name

class UserFactory(ModelFactory[User]):
    pass

# Either way seeds the shared Faker (same effect):
seed(42)
user1 = UserFactory.build()

UserFactory.seed_random(42)
user2 = UserFactory.build()  # same data as user1 if you seed the same before each
```

Use `UserFactory.__random_seed__ = 42` to seed once when the factory class is created, or call `seed(42)` / `UserFactory.seed_random(42)` before each build for identical builds.

## Publishing

Releases are built and published to PyPI via [GitHub Actions](.github/workflows/publish.yml). To publish:

1. Add a `PYPI_API_TOKEN` secret (PyPI API token) to the repo.
2. Create a GitHub release (tag e.g. `v0.1.0`). The workflow runs tests, builds the package, and uploads to PyPI.

To build and upload manually: `pip install build twine`, `python -m build`, `twine upload dist/*`.

## Links

- [Package plan](docs/capper_package_plan.md) — design and rationale
- [Roadmap](docs/ROADMAP.md) — development phases and status
- [Faker provider mapping](docs/FAKER_PROVIDERS.md) — type-to-provider reference
