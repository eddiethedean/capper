# Contributing to Capper

Thanks for your interest in contributing. This guide covers development setup and how to add new built-in types.

## Development setup

1. Clone the repo and install in editable mode with dev dependencies:

   ```bash
   pip install -e ".[dev]"
   ```

2. Run tests:

   ```bash
   pytest capper/tests -v
   ```

3. Lint and format:

   ```bash
   ruff check .
   ruff format .
   ```

4. Type-check:

   ```bash
   mypy capper
   ```

5. Build the docs (optional; requires `.[docs]`):

   ```bash
   pip install -e ".[dev,docs]"
   mkdocs serve
   ```

   Then open http://127.0.0.1:8000. Use `mkdocs build` to build static files to `site/`.

(CI runs on Python 3.9–3.12; see [.github/workflows/ci.yml](.github/workflows/ci.yml).)

## Adding a new built-in type

New semantic types are subclasses of `FakerType` with a Faker provider. To add one:

1. **Create or choose a module** under `capper/` (e.g. `capper/file.py`, `capper/person.py`). Add a class that subclasses `FakerType`, sets `faker_provider` to the Faker method name (e.g. `"file_path"`), and optionally `faker_kwargs`. Add a short docstring. See existing modules like [capper/person.py](capper/person.py) or [capper/file.py](capper/file.py) for the pattern.

2. **Export the type** in [capper/__init__.py](capper/__init__.py): add the import and add the name to `__all__` (keep `__all__` alphabetical).

3. **Register for Hypothesis** in [capper/strategies.py](capper/strategies.py): import the type and add it to the `_BUILTIN_TYPES` tuple so `st.from_type(YourType)` works.

4. **Document the provider** in [docs/FAKER_PROVIDERS.md](docs/FAKER_PROVIDERS.md): add a row under the right section with the type name and Faker provider (and any kwargs if relevant).

5. **Update the README** in [README.md](README.md): under “Available types”, add the new type(s) to the appropriate bullet (or add a new category).

6. **Add tests** in [capper/tests/test_types.py](capper/tests/test_types.py): add the type to the `test_type_generates_non_empty_string` parametrization list, and optionally to `test_model_factory_builds_capper_type` to confirm Polyfactory builds it.

7. Run `pytest capper/tests`, `ruff check .`, `ruff format .`, and `mypy capper` before opening a PR.

## Pull requests

- Branch from `main`.
- Ensure all tests pass and lint/type-check are clean.
- Keep changes focused; reference any related issues.

## Releases

When cutting a release, update [CHANGELOG.md](../CHANGELOG.md): move items from **Unreleased** into a new version heading and add the release date. See [README Publishing](../README.md#publishing).

For extending Capper with **third-party type packs** (your own package of `FakerType` subclasses), see [docs/extending.md](docs/extending.md).
