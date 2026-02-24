# Getting started

This guide gets you from zero to generating fake data with Capper in a few minutes.

## Install

You need **Python 3.9+**. Install Capper and its required backends:

```bash
pip install capper
```

For **Pydantic** models (used in most examples), also install the optional extra:

```bash
pip install capper[pydantic]
```

Capper depends on [Faker](https://faker.readthedocs.io/) and [Polyfactory](https://polyfactory.litestar.dev/); they are installed automatically.

## Your first model and factory

1. Define a Pydantic model (or dataclass) and use Capper types for fields you want to fake.
2. Create a Polyfactory factory for that model — no extra configuration needed.
3. Call `Factory.build()` to get one instance, or `Factory.batch(n)` for many.

**Example: a simple user**

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
    print("Name:", user.name)
    print("Email:", user.email)
```

Run this (from the repo root, with Capper installed):

```bash
python docs/examples/getting_started.py
```

You’ll see different name/email each run. Capper types are subclasses of `str`, so you can use them anywhere you’d use a string.

## What just happened?

- **`Name`** and **`Email`** are Capper types. Each is tied to a [Faker](https://faker.readthedocs.io/) provider (`name`, `email`).
- **Polyfactory**’s `ModelFactory` discovers Capper types and uses Capper’s shared Faker instance to generate values — no manual registration.
- **`UserFactory.build()`** creates one `User` with random but valid-looking name and email.

## Next steps

- [Models and factories](models_and_factories.md) — Pydantic vs dataclasses, batches, and more types.
- [Reproducible data](reproducible_data.md) — seeding for tests and demos.
- [Custom types](custom_types.md) — your own Faker-backed types and `faker_kwargs`.
