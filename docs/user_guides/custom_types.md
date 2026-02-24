# Custom types

You can add your own Faker-backed types by subclassing **`FakerType`** and setting **`faker_provider`** (and optionally **`faker_kwargs`**). They auto-register with Polyfactory when the class is defined.

## Using `faker_kwargs`

Existing Capper types use a fixed Faker method. To pass options (e.g. word count, format), subclass and set **`faker_kwargs`**:

```python
from capper.base import FakerType
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory


class ShortSentence(FakerType):
    """Sentence with exactly 5 words."""
    faker_provider = "sentence"
    faker_kwargs = {"nb_words": 5}


class Snippet(BaseModel):
    title: str  # Polyfactory default
    summary: ShortSentence


class SnippetFactory(ModelFactory[Snippet]):
    pass


if __name__ == "__main__":
    s = SnippetFactory.build()
    print("Summary (5 words):", s.summary)
```

## Defining a new type with `faker_provider`

Pick any Faker method name and assign it to **`faker_provider`**. The type will be registered for Polyfactory and (if Pydantic is installed) will validate as a string and coerce to your subclass.

```python
from capper.base import FakerType
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory


class CompanyName(FakerType):
    """Company name via Faker's company provider."""
    faker_provider = "company"


class Startup(BaseModel):
    name: CompanyName
    slogan: ShortSentence  # from above


class StartupFactory(ModelFactory[Startup]):
    pass


if __name__ == "__main__":
    startup = StartupFactory.build()
    print(startup.name, "—", startup.slogan)
```

## Combining provider and kwargs

Use both when the Faker method accepts options (e.g. date format, pattern):

```python
from capper.base import FakerType
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory


class USDate(FakerType):
    """Date string in MM/DD/YYYY format."""
    faker_provider = "date"
    faker_kwargs = {"pattern": "%m/%d/%Y"}


class Event(BaseModel):
    name: str
    date: USDate


class EventFactory(ModelFactory[Event]):
    pass


if __name__ == "__main__":
    e = EventFactory.build()
    print(e.name, e.date)
```

## Run the examples

From the repo root (with Capper installed):

```bash
python docs/examples/custom_types.py
```

For the list of Faker providers and their arguments, see [Faker’s documentation](https://faker.readthedocs.io/) and [FAKER_PROVIDERS.md](../FAKER_PROVIDERS.md).
