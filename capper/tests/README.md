# Capper tests

- **test_types.py** — Faker provider availability for all capper types; `faker_kwargs`; seed reproducibility; ModelFactory build with a subset of types (registration).
- **test_polyfactory_integration.py** — Pydantic + ModelFactory (User build/batch); shared Faker (seed_random vs capper.seed); DataclassFactory with capper types; auto-registration (Contact/PhoneNumber).

Fixtures (e.g. `seeded_faker`) live in **conftest.py**.
