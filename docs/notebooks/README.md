# Example notebooks

Jupyter notebooks demonstrating Capper usage.

| Notebook | Description |
|----------|-------------|
| [01_getting_started.ipynb](01_getting_started.ipynb) | First Pydantic model with Name and Email. |
| [02_models_and_batch.ipynb](02_models_and_batch.ipynb) | Pydantic, dataclass, `batch()`, mixing Capper and built-in types. |
| [03_reproducible_data.ipynb](03_reproducible_data.ipynb) | Seeding with `seed()` and `seed_random()`. |
| [04_custom_types.ipynb](04_custom_types.ipynb) | Custom `FakerType` subclasses and `faker_kwargs`. |

Run from the repo root with the project venv:

```bash
.venv/bin/jupyter notebook
```

Then open a notebook from this directory (`docs/notebooks`).
