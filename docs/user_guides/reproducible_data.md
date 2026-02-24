# Reproducible data (seeding)

For tests or demos you often want the same fake data every run. Capper and Polyfactory share one Faker instance, so a single seed gives you reproducible Capper types and built-in types (`str`, `int`, etc.).

## Using `seed()`

Call **`capper.seed(seed_value)`** before building. The same integer seed produces the same sequence of values.

```python
from capper import seed, Name, Email
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel


class User(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[User]):
    pass


if __name__ == "__main__":
    seed(42)
    user1 = UserFactory.build()
    seed(42)
    user2 = UserFactory.build()
    assert user1.name == user2.name and user1.email == user2.email
    print("Reproducible:", user1.name, user1.email)
```

## Using `Factory.seed_random()`

Polyfactory’s **`YourFactory.seed_random(seed_value)`** seeds the same shared Faker instance. So you can use either:

- **`seed(42)`** then **`UserFactory.build()`**, or  
- **`UserFactory.seed_random(42)`** then **`UserFactory.build()`**

Same seed ⇒ same data.

```python
from capper import seed, Name
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel


class User(BaseModel):
    name: Name


class UserFactory(ModelFactory[User]):
    pass


if __name__ == "__main__":
    seed(42)
    a = UserFactory.build()
    UserFactory.seed_random(42)
    b = UserFactory.build()
    assert a.name == b.name
    print("Same name:", a.name)
```

## Seeding once on the factory

Set **`YourFactory.__random_seed__ = 42`** when you define the factory. Every build will use that seed (reproducible across the process).

```python
from capper import Name
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel


class User(BaseModel):
    name: Name


class UserFactory(ModelFactory[User]):
    __random_seed__ = 12345


if __name__ == "__main__":
    u1 = UserFactory.build()
    u2 = UserFactory.build()
    # With fixed seed, u1.name and u2.name are deterministic
    print(u1.name, u2.name)
```

## Run the examples

From the repo root (with Capper installed):

```bash
python docs/examples/reproducible_data.py
```

See [Getting started](getting_started.md) for install and [Custom types](custom_types.md) for extending Capper.
