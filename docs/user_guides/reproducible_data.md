# Reproducible data (seeding)

For tests or demos you often want the same fake data every run. Capper and Polyfactory share the same per-thread Faker instance via a proxy, so within a given thread a single seed gives you reproducible Capper types and built-in types (`str`, `int`, etc.).

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

Polyfactory’s **`YourFactory.seed_random(seed_value)`** seeds the same per-thread Faker instance (through the shared proxy). So you can use either:

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

## Locales and custom Faker

Capper and Polyfactory both use a single shared Faker instance. To use a **custom locale** (e.g. German names and addresses) everywhere, replace that instance so both Capper types and Polyfactory’s built-in types use it.

**Option 1: `use_faker()`** — one call updates both Capper and Polyfactory:

```python
from faker import Faker
from capper import use_faker, Name, Address
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel

use_faker(Faker("de_DE"))

class Person(BaseModel):
    name: Name
    address: Address

class PersonFactory(ModelFactory[Person]):
    pass

p = PersonFactory.build()  # German-style name and address
```

**Option 2: Set both manually** — set the global Capper faker and Polyfactory’s default so seeds and locale stay in sync:

```python
from faker import Faker
import capper
from polyfactory.factories.base import BaseFactory

my_faker = Faker("de_DE")
capper.faker = my_faker
BaseFactory.__faker__ = my_faker
# then use capper types and factories as usual
```

If you only set **`YourFactory.__faker__ = Faker('de_DE')`** on a specific factory, Polyfactory’s built-in types will use that locale, but Capper-generated fields still use the global `capper.faker`. For full locale control, use `use_faker(my_faker)` or set both as above.

**Multi-threaded tests:** Each thread has its own Faker. In multi-threaded tests, call **`seed(n)`** or **`use_faker(instance)`** inside each thread that needs reproducible or locale-specific data.

## Run the examples

From the repo root (with Capper installed):

```bash
python docs/examples/reproducible_data.py
```

See [Getting started](getting_started.md) for install and [Custom types](custom_types.md) for extending Capper.
