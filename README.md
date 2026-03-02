# Capper

[![PyPI](https://img.shields.io/pypi/v/capper.svg)](https://pypi.org/project/capper/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://pypi.org/project/capper/)
[![CI](https://img.shields.io/github/actions/workflow/status/eddiethedean/capper/ci.yml?branch=main&label=CI%20(lint%2C%20types%2C%20tests%2C%20docs))](https://github.com/eddiethedean/capper/actions/workflows/ci.yml)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy-lang.org/)

Semantic, typed wrappers for [Faker](https://faker.readthedocs.io/) with automatic [Polyfactory](https://polyfactory.litestar.dev/) integration.

**Source:** [github.com/eddiethedean/capper](https://github.com/eddiethedean/capper)

## CI pipeline

The `ci.yml` workflow runs on pushes and PRs to `main` and includes:

- **Linting:** `ruff check .` and `ruff format --check .`
- **Type checking:** `mypy capper`
- **Tests:** `pytest -n auto capper/tests -v -m "not benchmark" --cov=capper --cov-report=term-missing --cov-fail-under=98`
- **Docs:** `mkdocs build --strict`

## Why Capper?

- **Zero config** — Import a type; Polyfactory uses the right Faker provider. No manual registration.
- **Typed** — Use `Name`, `Email`, `PhoneNumber`, etc. in your models for clear intent and IDE support.
- **Multi-backend** — Works with Pydantic, dataclasses, attrs, and other [Polyfactory-supported](https://polyfactory.litestar.dev/) model types.
- **Thread-safe** — Per-thread Faker via a proxy; seeding and locales are isolated per thread, so concurrent tests are safe.
- **Optional Pydantic** — Install `capper` alone for dataclasses/attrs; add `capper[pydantic]` when you use Pydantic models.

## Install

```bash
pip install capper
```

Requires **Python 3.10+**, **Faker >= 20.0**, and **Polyfactory >= 2.0**. Optional extras:

- **Pydantic** (for Pydantic models): `pip install capper[pydantic]`
- **Hypothesis** (for property-based tests with `st.from_type(...)`): `pip install capper[hypothesis]`

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

**New to Capper?** See the [Getting started](docs/user_guides/getting_started.md) guide and run the examples in `docs/examples/`.

## Available types

- **Person**: `Name`, `FirstName`, `LastName`, `Job`
- **Geo**: `Address`, `City`, `Country`
- **Internet**: `Email`, `URL`, `IP`, `UserName`
- **Commerce**: `Company`, `Product`, `Currency`, `Price`
- **Date/time**: `Date`, `DateTime`, `Time`
- **Text**: `Paragraph`, `Sentence`
- **Phone**: `PhoneNumber`, `CountryCallingCode`
- **Finance**: `CreditCardNumber`, `CreditCardExpiry`, `CreditCardProvider`
- **File**: `FilePath`, `FileName`, `FileExtension`
- **Misc**: `UUID`
- **Color**: `HexColor`
- **Barcode**: `EAN13`, `EAN8`

Import from the top level: `from capper import Name, Email, Address, ...`  
See [docs/FAKER_PROVIDERS.md](https://github.com/eddiethedean/capper/blob/main/docs/FAKER_PROVIDERS.md) for the Faker provider used by each type.

**Optional kwargs:** Subclass `FakerType` and set `faker_kwargs` to pass arguments to the Faker provider (e.g. `faker_kwargs = {"nb_words": 10}` for `Sentence`).

**Custom types:** Subclass `FakerType`, set `faker_provider` to the Faker method name (e.g. `"company"`), and optionally `faker_kwargs`. The type auto-registers with Polyfactory when the class is defined.

## CLI

Generate fake values from the command line:

```bash
capper generate Name Email --count 5
capper generate Name Email --count 3 --seed 42
```

Use `-n`/`--count` for the number of rows and `-s`/`--seed` for reproducible output. Type names are the same as the Python types (e.g. `Name`, `Email`, `Address`).

## Compatibility

Capper targets **Python 3.10+**, **Faker >= 20.0**, and **Polyfactory >= 2.0**. For version ranges, upgrade guidance, and the deprecation policy, see [Compatibility](docs/compatibility.md).

## What's new in 0.4.0

- **Thread safety:** Capper is now thread-safe via a per-thread Faker proxy; `seed()` and `use_faker()` only affect the current thread.
- **Reliability and coverage:** Phase 9 adds a coverage gate (≥ 98% for `capper/`), targeted edge-case tests, and a lightweight performance check in CI.
- **Tooling and docs:** CI runs Ruff, mypy, tests (with coverage gate), and a strict MkDocs build on all supported Python versions; docs and roadmap have been updated to reflect Phase 9.

## Development

```bash
pip install -e ".[dev]"
pytest capper/tests
```

Lint and type-check: `ruff check .`, `ruff format .`, `mypy capper`.

Run tests with coverage: `pytest capper/tests --cov=capper --cov-report=term-missing`. CI requires coverage ≥ 98% for the `capper/` package (`--cov-fail-under=98`).

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

Use `UserFactory.__random_seed__ = 42` to seed once when the factory class is created, or call `seed(42)` / `UserFactory.seed_random(42)` before each build for identical builds. For a custom locale (e.g. German names), use **`use_faker(Faker('de_DE'))`** so both Capper and Polyfactory use the same Faker instance; see [Reproducible data](docs/user_guides/reproducible_data.md#locales-and-custom-faker).

## Publishing

Releases are built and published to PyPI via [GitHub Actions](https://github.com/eddiethedean/capper/blob/main/.github/workflows/publish.yml). To publish:

1. Update [CHANGELOG.md](CHANGELOG.md): move Unreleased entries into a new version section and date it.
2. Add a `PYPI_API_TOKEN` secret (PyPI API token) to the repo.
3. Create a GitHub release (tag e.g. `v0.4.0`). The workflow runs tests, builds the package, and uploads to PyPI.

To build and upload manually: `pip install build twine`, `python -m build`, `twine upload dist/*`.

## Documentation

- **[Docs index](docs/README.md)** — overview and links to all documentation
- **[API reference](docs/api.md)** — generated API docs (build with `mkdocs serve`; see [Contributing](CONTRIBUTING.md))
- **[Contributing](CONTRIBUTING.md)** — dev setup and how to add new types
- **User guides** (step-by-step, with runnable examples):
  - [Getting started](docs/user_guides/getting_started.md) — install, first model, first factory
  - [Models and factories](docs/user_guides/models_and_factories.md) — Pydantic, dataclasses, batches
  - [Reproducible data](docs/user_guides/reproducible_data.md) — seeding for tests and demos
  - [Custom types](docs/user_guides/custom_types.md) — `FakerType` subclasses and `faker_kwargs`
- [Package plan](docs/capper_package_plan.md) — design and rationale
- [Roadmap](docs/ROADMAP.md) — development phases and status
- [Faker provider mapping](docs/FAKER_PROVIDERS.md) — which Faker method each type uses
- [Example notebooks](docs/notebooks/README.md) — Jupyter notebooks in `docs/notebooks/`
