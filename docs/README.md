# Capper documentation

Documentation for the [Capper](https://github.com/eddiethedean/capper) package — semantic Faker types with automatic Polyfactory integration.

| Document | Description |
|----------|-------------|
| [../README.md](../README.md) | Install, usage, examples, and publishing. Start here. |
| [capper_package_plan.md](capper_package_plan.md) | Design, layout, registration, and development plan. |
| [ROADMAP.md](ROADMAP.md) | Phases, current status, and release milestones. |
| [FAKER_PROVIDERS.md](FAKER_PROVIDERS.md) | Mapping of each capper type to its Faker provider. |
| [notebooks/README.md](notebooks/README.md) | Example Jupyter notebooks. |

## User guides

Step-by-step guides with runnable examples (run from repo root with Capper installed: `python docs/examples/<name>.py`):

| Guide | Description |
|-------|-------------|
| [user_guides/getting_started.md](user_guides/getting_started.md) | Install, first Pydantic model, first factory. |
| [user_guides/models_and_factories.md](user_guides/models_and_factories.md) | Pydantic vs dataclasses, batches, mixing Capper and built-in types. |
| [user_guides/reproducible_data.md](user_guides/reproducible_data.md) | Seeding with `seed()`, `seed_random()`, and `__random_seed__`. |
| [user_guides/custom_types.md](user_guides/custom_types.md) | Custom `FakerType` subclasses and `faker_kwargs`. |

Runnable scripts for each guide live in [docs/examples/](examples/).

## Types and API

For the full list of Capper types and the Faker provider used by each, see
[FAKER_PROVIDERS.md](FAKER_PROVIDERS.md). Import types from the top level: ``from capper import Name, Email, ...``.

---

**Quick links**

- **Using capper:** See the main [README](../README.md) for install and examples (Pydantic, dataclass, seed, kwargs).
- **User guides:** [getting_started](user_guides/getting_started.md) → [models and factories](user_guides/models_and_factories.md) → [reproducible data](user_guides/reproducible_data.md) → [custom types](user_guides/custom_types.md).
- **How it works:** [Package plan](capper_package_plan.md) — `FakerType`, auto-registration, optional Pydantic.
- **What’s next:** [Roadmap](ROADMAP.md) — phases and versions.
- **Type → Faker:** [Faker providers](FAKER_PROVIDERS.md) — which Faker method each type uses.
