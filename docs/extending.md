# Extending Capper: third-party type packs

You can ship your own **type pack**: a separate Python package that defines `FakerType` subclasses and re-exports them. Users install your pack and use those types in their models; Polyfactory will generate values for them automatically because subclasses register on class definition.

## How type packs work

1. Your package depends on `capper` (e.g. `install_requires = ["capper>=0.2"]`).
2. You define one or more classes that subclass `capper.FakerType`, set `faker_provider` (and optionally `faker_kwargs`), and optionally re-export them from your package’s top-level.
3. Users install your pack and use your types in Pydantic models, dataclasses, or attrs. When they use a Polyfactory factory for that model, Polyfactory will call your type’s provider—no extra registration step needed.

Example (inside your package):

```python
# my_capper_pack/types.py
from capper import FakerType

class ISBN(FakerType):
    """Fake ISBN. Uses Faker provider isbn13 (or similar)."""
    faker_provider = "isbn13"

class AvatarURL(FakerType):
    faker_provider = "image_url"
    faker_kwargs = {"width": 64, "height": 64}
```

Users then do:

```python
from pydantic import BaseModel
from my_capper_pack import ISBN, AvatarURL
from polyfactory.factories.pydantic_factory import ModelFactory

class Book(BaseModel):
    isbn: ISBN
    cover: AvatarURL

class BookFactory(ModelFactory[Book]):
    pass

book = BookFactory.build()  # works
```

## Hypothesis support (optional)

If your pack’s users want to use Hypothesis’s `st.from_type(YourType)`, they (or you) can register a strategy after defining the type:

```python
from hypothesis.strategies import register_type_strategy
import capper.strategies as capper_strategies
from my_capper_pack import ISBN

register_type_strategy(ISBN, capper_strategies.for_type(ISBN))
```

Then `st.from_type(ISBN)` will work. You can do this in your package’s `__init__.py` so that importing your types automatically registers them with Hypothesis.

No changes to Capper itself are required; this is a documentation-only pattern.

## Known type packs and integrations

Capper is designed to be extended. If you publish a type pack or integration that builds on Capper,
you can open a pull request to add a short entry here with:

- Package name and link
- Short description (1–2 sentences)
- Maintainer or organization (optional)

Examples of integrations that fit well:

- Domain-specific type packs (e.g. finance, healthcare, gaming)
- Framework integrations (e.g. helper packages for FastAPI or Django test setups)

