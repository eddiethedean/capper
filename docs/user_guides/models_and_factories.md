# Models and factories

Capper works with any model type that Polyfactory supports: Pydantic, dataclasses, and attrs. Use the matching factory class and the same Capper types.

## Pydantic models

Use **`ModelFactory`** from `polyfactory.factories.pydantic_factory`. Requires `capper[pydantic]`.

```python
from pydantic import BaseModel
from capper import Name, Email, Address, PhoneNumber
from polyfactory.factories.pydantic_factory import ModelFactory


class Contact(BaseModel):
    name: Name
    email: Email
    address: Address
    phone: PhoneNumber


class ContactFactory(ModelFactory[Contact]):
    pass


if __name__ == "__main__":
    contact = ContactFactory.build()
    print(contact.model_dump())
    # Batch of 3
    for c in ContactFactory.batch(3):
        print(c.name, "—", c.email)
```

## Dataclasses (no Pydantic)

Use **`DataclassFactory`** from `polyfactory.factories`. Plain `pip install capper` is enough.

```python
from dataclasses import dataclass
from capper import Name, Email
from polyfactory.factories import DataclassFactory


@dataclass
class Person:
    name: Name
    email: Email


class PersonFactory(DataclassFactory[Person]):
    pass


if __name__ == "__main__":
    person = PersonFactory.build()
    print(person.name, person.email)
    for p in PersonFactory.batch(2):
        print(p)
```

## Mixing Capper types with built-in types

You can use Capper types alongside normal types. Polyfactory will generate values for both; Capper types use Faker, other types use Polyfactory’s defaults.

```python
from pydantic import BaseModel
from capper import Company, Product, Price
from polyfactory.factories.pydantic_factory import ModelFactory


class Listing(BaseModel):
    company: Company
    product: Product
    price: Price
    quantity: int  # built-in; Polyfactory generates an int


class ListingFactory(ModelFactory[Listing]):
    pass


if __name__ == "__main__":
    listing = ListingFactory.build()
    print(f"{listing.company}: {listing.product} @ {listing.price} x {listing.quantity}")
```

## Run the examples

From the repo root (with Capper installed):

```bash
python docs/examples/models_and_factories.py
```

See [Getting started](getting_started.md) for install and [FAKER_PROVIDERS.md](../FAKER_PROVIDERS.md) for the full list of Capper types and their Faker providers.
