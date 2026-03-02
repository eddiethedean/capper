# Capper

[![PyPI](https://img.shields.io/pypi/v/capper.svg)](https://pypi.org/project/capper/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://pypi.org/project/capper/)
[![CI](https://img.shields.io/github/actions/workflow/status/eddiethedean/capper/ci.yml?branch=main&label=CI%20(lint%2C%20types%2C%20tests%2C%20docs))](https://github.com/eddiethedean/capper/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/capper/badge/?version=latest)](https://capper.readthedocs.io/en/latest/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![mypy](https://img.shields.io/badge/mypy-checked-blue.svg)](https://mypy-lang.org/)

Semantic, typed wrappers for [Faker](https://faker.readthedocs.io/) with automatic [Polyfactory](https://polyfactory.litestar.dev/) integration.

**Source:** [github.com/eddiethedean/capper](https://github.com/eddiethedean/capper) · **Docs:** [capper.readthedocs.io](https://capper.readthedocs.io/en/latest/)

---

## What is Capper?

Capper gives you **semantic Faker types** (like `Name`, `Email`, `Price`) that:

- **Zero configuration**: just import a type and use it in your models; Polyfactory knows how to generate values.
- **Strongly typed**: your models communicate intent instead of bare `str` fields.
- **Multi-backend**: works with Pydantic, dataclasses, attrs, and other Polyfactory-supported model types.
- **Thread-safe & reproducible**: per-thread Faker with helpers for seeding and locales.

You import types from the top level:

```python
from capper import Name, Email
```

and use them anywhere you would use a string (or the relevant base type).

For the full story, see the **[Capper documentation](https://capper.readthedocs.io/en/latest/)**.

---

## Installation

```bash
pip install capper
```

- **Python**: 3.10+
- **Core deps**: Faker ≥ 20.0, Polyfactory ≥ 2.0 (installed automatically)
- **Optional extras**:
  - **Pydantic support**: `pip install capper[pydantic]`
  - **Hypothesis strategies**: `pip install capper[hypothesis]`

Step‑by‑step instructions live in the **[Getting started guide](https://capper.readthedocs.io/en/latest/user_guides/getting_started/)**.

---

## Quick example

Using Capper with a Pydantic model and Polyfactory:

```python
from pydantic import BaseModel
from capper import Name, Email
from polyfactory.factories.pydantic_factory import ModelFactory


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    pass


if __name__ == "__main__":
    user = UserFactory.build()
    print(user)
```

For more patterns (dataclasses and attrs, FastAPI, Django-style service layers, seeding, and custom types), see the **[User guides](https://capper.readthedocs.io/en/latest/#user-guides)**.

---

## CLI

Generate fake values from the command line:

```bash
capper generate Name Email --count 5
capper generate Name Email --count 3 --seed 42
```

- **Types**: same names as the Python types (e.g. `Name`, `Email`, `Address`).
- **Flags**:
  - **`-n` / `--count`**: number of rows
  - **`-s` / `--seed`**: seed for reproducible output

CLI usage examples are covered in the getting started and models/factories guides on Read the Docs.

---

## Types and providers

Capper exports all public types from the top level, for example:

```python
from capper import Name, FirstName, LastName, Address, Email, Price
```

To see:

- the **full list of types**, and  
- which **Faker provider** each one uses,

visit the **[Faker providers](https://capper.readthedocs.io/en/latest/FAKER_PROVIDERS/)** page.

---

## Documentation

Most detail lives in the hosted docs:

- **Docs home**: <https://capper.readthedocs.io/en/latest/>
- **User guides** (with runnable examples):
  - [Getting started](https://capper.readthedocs.io/en/latest/user_guides/getting_started/)
  - [Models and factories](https://capper.readthedocs.io/en/latest/user_guides/models_and_factories/)
  - [Reproducible data](https://capper.readthedocs.io/en/latest/user_guides/reproducible_data/)
  - [Custom types](https://capper.readthedocs.io/en/latest/user_guides/custom_types/)
  - [FastAPI + Pydantic](https://capper.readthedocs.io/en/latest/user_guides/fastapi_pydantic/)
  - [Django patterns](https://capper.readthedocs.io/en/latest/user_guides/django_patterns/)
  - [Dataclasses and attrs](https://capper.readthedocs.io/en/latest/user_guides/dataclasses_and_attrs/)
  - [Test setup templates](https://capper.readthedocs.io/en/latest/user_guides/test_setup_templates/)
  - [Project structure](https://capper.readthedocs.io/en/latest/user_guides/project_structure/)
- **Types & API**:
  - [Faker provider mapping](https://capper.readthedocs.io/en/latest/FAKER_PROVIDERS/)
  - [API reference](https://capper.readthedocs.io/en/latest/api/)
- **Design & roadmap**:
  - [Package plan](https://capper.readthedocs.io/en/latest/capper_package_plan/)
  - [Roadmap](https://capper.readthedocs.io/en/latest/ROADMAP/)
- **Stability & support**:
  - [Compatibility](https://capper.readthedocs.io/en/latest/compatibility/)
  - [Security](https://capper.readthedocs.io/en/latest/SECURITY/)

If you are unsure where to start, begin at the docs home and follow the “User guides” flow.

---

## Compatibility and support

- **Runtime targets**: Python 3.10+, Faker ≥ 20.0, Polyfactory ≥ 2.0.
- **Semantic versioning**: Capper follows SemVer; the 1.x line maintains a stable public API.
- **Support & backports**: policy, supported versions, and backport rules are described in the **[Compatibility](https://capper.readthedocs.io/en/latest/compatibility/)** docs.

---

## Development

```bash
pip install -e ".[dev]"
pytest capper/tests
```

- **Lint & format**: `ruff format .` and `ruff check .`
- **Type checking**: `mypy capper`
- **Coverage**:

  ```bash
  pytest capper/tests --cov=capper --cov-report=term-missing --cov-fail-under=98
  ```

For contributor guidance (branching, testing, release process), see `CONTRIBUTING.md` and the maintenance‑oriented guides on Read the Docs.

---

## Security

- **CI security checks**:
  - `pip-audit` runs in CI to scan dependencies.
  - A scheduled “latest deps” workflow tests Capper against current Faker and Polyfactory releases.
- **Policy & reporting**: see the **[Security page](https://capper.readthedocs.io/en/latest/SECURITY/)** for how to report issues and which versions are supported.

---

## License

Capper is licensed under the **MIT License**. See `LICENSE` for details.

# Capper

[![PyPI](https://img.shields.io/pypi/v/capper.svg)](https://pypi.org/project/capper/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://pypi.org/project/capper/)
[![CI](https://img.shields.io/github/actions/workflow/status/eddiethedean/capper/ci.yml?branch=main&label=CI%20(lint%2C%20types%2C%20tests%2C%20docs))](https://github.com/eddiethedean/capper/actions/workflows/ci.yml)
[![Docs](https://readthedocs.org/projects/capper/badge/?version=latest)](https://capper.readthedocs.io/en/latest/)
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

- **Quick start**: define a Pydantic model or dataclass using Capper types (e.g. `Name`, `Email`), create a Polyfactory factory, and call `Factory.build()` / `Factory.batch()`.
- **Guided examples**: see the docs:
  - [Getting started](docs/user_guides/getting_started.md) — install, first model, first factory
  - [Models and factories](docs/user_guides/models_and_factories.md) — Pydantic vs dataclasses, batches, mixing Capper and built-in types

## Available types

Import from the top level: `from capper import Name, Email, Address, ...`.  
See the **[Faker provider mapping](docs/FAKER_PROVIDERS.md)** (or the hosted docs) for the full list of types and which Faker provider each uses.

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

Capper targets **Python 3.10+**, **Faker >= 20.0**, and **Polyfactory >= 2.0**. For version ranges, upgrade guidance, the versioning policy, and the deprecation policy, see [Compatibility](docs/compatibility.md).

### Support & maintenance

- Supported Python and dependency versions, along with backport expectations for the 1.0.x line, are documented in [docs/compatibility.md](docs/compatibility.md).
- Critical bug fixes and compatibility fixes may be backported to the latest 1.0.x release; new features land in minor releases.

## Security

- The CI pipeline includes a dependency vulnerability scan using `pip-audit` (see `.github/workflows/ci.yml`).
- A separate compatibility workflow (`compat-latest.yml`) runs tests against the latest Faker and Polyfactory versions.
- For details on supported versions and how to report security issues, see [SECURITY.md](SECURITY.md).

## What's new in 1.0.0

- **Production-ready, stable API:** Capper 1.0.0 promotes the 0.5.x feature set (Phases 9–11) to a stable, production-ready API with documented compatibility and versioning guarantees.
- **Governance and maintenance:** Added governance and maintenance documentation (issue/PR templates, code of conduct, maintainer expectations, release and maintenance review checklists) to support long-term evolution.
- **Security and compatibility:** CI now includes `pip-audit` and a scheduled latest-deps workflow; the security policy and compatibility docs describe how issues are reported, triaged, and backported.

## Development

```bash
pip install -e ".[dev]"
pytest capper/tests
```

Lint and type-check: `ruff check .`, `ruff format .`, `mypy capper`.

Run tests with coverage: `pytest capper/tests --cov=capper --cov-report=term-missing`. CI requires coverage ≥ 98% for the `capper/` package (`--cov-fail-under=98`).

For seeding, locales, and reproducible test data patterns, see **[Reproducible data](docs/user_guides/reproducible_data.md)**.

## Publishing

Releases are built and published to PyPI via [GitHub Actions](https://github.com/eddiethedean/capper/blob/main/.github/workflows/publish.yml). To publish:

1. Update [CHANGELOG.md](CHANGELOG.md): move Unreleased entries into a new version section and date it.
2. Add a `PYPI_API_TOKEN` secret (PyPI API token) to the repo.
3. Create a GitHub release (tag e.g. `v0.4.1`). The workflow runs tests, builds the package, and uploads to PyPI.

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
  - [FastAPI + Pydantic](docs/user_guides/fastapi_pydantic.md) — API payloads and tests using Capper-backed Pydantic models
  - [Django patterns](docs/user_guides/django_patterns.md) — Django-style schemas, factories, and service tests
  - [Dataclasses and attrs](docs/user_guides/dataclasses_and_attrs.md) — non-Pydantic projects with `DataclassFactory`
  - [Test setup templates](docs/user_guides/test_setup_templates.md) — pytest/Hypothesis fixtures and seeding patterns
  - [Project structure](docs/user_guides/project_structure.md) — organizing Capper types, factories, and type packs
- [Package plan](docs/capper_package_plan.md) — design and rationale
- [Roadmap](docs/ROADMAP.md) — development phases and status
- [Faker provider mapping](docs/FAKER_PROVIDERS.md) — which Faker method each type uses
- [Example notebooks](docs/notebooks/README.md) — Jupyter notebooks in `docs/notebooks/`
