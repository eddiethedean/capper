## Dataclasses and attrs-heavy codebases

Capper works well even when you do not use Pydantic at all. This guide shows patterns for **dataclasses** and **attrs** using Polyfactory.

### Dataclasses with `DataclassFactory`

```python
from dataclasses import dataclass

from capper import Email, Name
from polyfactory.factories import DataclassFactory


@dataclass
class Person:
    name: Name
    email: Email


class PersonFactory(DataclassFactory[Person]):
    __random_seed__ = 7
```

Use the factory in tests:

```python
def test_person_factory_builds() -> None:
    person = PersonFactory.build()
    assert isinstance(person.name, str)
    assert isinstance(person.email, str)
```

### attrs classes

If you prefer [attrs](https://www.attrs.org/), use `attrs.define` and the same `DataclassFactory`:

```python
import attrs

from capper import Name
from polyfactory.factories import DataclassFactory


@attrs.define
class Customer:
    name: Name


class CustomerFactory(DataclassFactory[Customer]):
    pass
```

### Mixing Capper types with built-in types

Capper types behave like strings (or whatever base type you choose), so you can mix them with normal fields:

```python
@dataclass
class Order:
    customer_name: Name
    total_cents: int
```

`DataclassFactory[Order]` will use Capper for `customer_name` and Polyfactory defaults for `total_cents`.

### Running the example

From the repo root (with Capper installed):

```bash
python docs/examples/dataclasses_and_attrs.py
```

The example script demonstrates both dataclasses and attrs usage. See also:

- [Getting started](getting_started.md)
- [Models and factories](models_and_factories.md)
- [Custom types](custom_types.md)
