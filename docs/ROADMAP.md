# Capper roadmap

High-level development phases and current status. See [capper_package_plan.md](../capper_package_plan.md) for full design and [README.md](../README.md) for usage.

---

## Current status

- **Initial structure** in place: package layout, `FakerType` base, core semantic types, tests, and examples.
- **Phase 1 (MVP)** is in progress: base class and auto-registration are done; expanding to 15–20 core types and stabilizing tests.

---

## Phase 1 — MVP

- [x] Implement `FakerType` base class with automatic Polyfactory registration.
- [x] Implement initial set of core semantic types (person, geo, internet, commerce, date/time).
- [ ] Expand to 15–20 core semantic types as needed.
- [x] Unit tests for types and Polyfactory integration.

---

## Phase 2 — Full coverage

- [ ] Add remaining Faker providers (Commerce, Text, Date/Time, Phone, Credit cards).
- [ ] Ensure all types auto-register on import.
- [ ] Align type names and providers with Faker’s API across locales where relevant.

---

## Phase 3 — Packaging

- [x] `pyproject.toml` with Faker, Polyfactory, and Pydantic dependencies.
- [ ] Publish to PyPI.
- [x] Usage examples in repo (e.g. `capper/examples/user_factory.py`).

---

## Phase 4 — Optional enhancements

- [ ] Support Faker provider kwargs (e.g. min/max lengths, locales).
- [ ] Auto-sync or compatibility notes with new Faker releases.
- [ ] (Future) Hypothesis strategies, custom type registration, optional CLI.

---

## Milestones / releases

| Version | Focus |
|--------|--------|
| 0.1.0  | Initial structure, MVP types, tests, examples (current). |
| 0.2.0  | Phase 2 coverage and packaging (PyPI). |
| 0.3.0+ | Phase 4 enhancements as needed. |

---

*Last updated with initial structure and roadmap.*
