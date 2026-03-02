## Test setup templates (pytest and Hypothesis)

This guide collects small, copy/paste-friendly templates for common test setups
when using Capper with Polyfactory, pytest, and optionally Hypothesis.

All examples assume Capper is installed and tests run under **Python 3.10+**.

### Global seeding in pytest

Put this in your `conftest.py` to make Capper-generated data reproducible across a test run:

```python
import pytest

from capper import seed


@pytest.fixture(autouse=True, scope="session")
def seed_capper_once() -> None:
    # Seed Capper's per-thread Faker for deterministic runs
    seed(12345)
```

### Per-test seeding fixture

If you want each test to control its own seed:

```python
import itertools

import pytest

from capper import seed

_seed_counter = itertools.count(1)


@pytest.fixture(autouse=True)
def deterministic_faker_per_test() -> None:
    seed(next(_seed_counter))
```

This gives each test a different but deterministic seed while avoiding collisions.

### Shared base factory

For Pydantic models:

```python
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory


class BaseTestFactory(ModelFactory[BaseModel]):
    """Base factory for all tests."""

    __random_seed__ = 42
```

Subclasses inherit the seed and common configuration.

### Hypothesis strategies

To use Capper types with Hypothesis’s `st.from_type()`:

```python
from hypothesis.strategies import register_type_strategy

import capper.strategies as capper_strategies
from capper import Name


def register_strategies() -> None:
    register_type_strategy(Name, capper_strategies.for_type(Name))
```

Call `register_strategies()` once at import time in your tests (for example in `conftest.py`).

### Running the example

From the repo root (with Capper installed):

```bash
python docs/examples/test_setup_templates.py
```

The example script mirrors these patterns without depending on pytest or Hypothesis.

Example output (values will vary):

```text
--- Using factory-level seed ---
{'name': 'Angela Brennan', 'email': 'zwebb@example.net'}
{'name': 'Robert Bruce', 'email': 'brewermary@example.org'}

--- Overriding with global seed() ---
{'name': 'Allison Hill', 'email': 'donaldgarcia@example.net'}
{'name': 'Allison Hill', 'email': 'donaldgarcia@example.net'}
```

See also:

- [Reproducible data](reproducible_data.md)
- [Custom types](custom_types.md)
- [Compatibility](../compatibility.md)
