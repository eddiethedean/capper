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

## How this fits into Capper's design

Capper’s core pieces work together to keep your types simple while handling the wiring for you:

- **`FakerType`**: a thin `str` subclass that only needs `faker_provider` (and optional `faker_kwargs`). When you subclass it, Capper automatically:\n  - Registers a provider with Polyfactory so factories can generate values.\n  - Installs a Pydantic schema hook (when `capper[pydantic]` is installed) so your type validates as `str` and is coerced to your subclass.\n- **Shared Faker instance**: Capper and Polyfactory share one Faker via the module-level `faker`, `seed()`, and `use_faker()` helpers; seeding once controls both built-in fields and Capper types.\n- **Type registry and Hypothesis strategies**: Capper discovers all exported `FakerType` subclasses from the package’s public API and registers Hypothesis strategies so `st.from_type(YourFakerType)` works once you `import capper.strategies`.\n\nAs long as you follow the simple contract (subclass `FakerType`, set `faker_provider`, and optionally `faker_kwargs`), the rest of the system—factories, validation, CLI, and property-based tests—stays consistent and extensible without extra configuration.

## Run the examples

From the repo root (with Capper installed):

```bash
python docs/examples/custom_types.py
```

Example output (values will vary):

```text
--- ShortSentence (faker_kwargs) ---
Summary (5 words): Table and house.

--- CompanyName + ShortSentence ---
Hicks-Nash — Risk somebody finally someone.

--- USDate (provider + kwargs) ---
BdeWHGKTkyEnrYblLocN 10/29/1983
```

For the list of Faker providers and their arguments, see [Faker’s documentation](https://faker.readthedocs.io/) and [FAKER_PROVIDERS.md](../FAKER_PROVIDERS.md).
