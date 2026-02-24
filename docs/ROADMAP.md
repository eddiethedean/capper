# Capper roadmap

High-level development phases and current status. See [capper_package_plan.md](capper_package_plan.md) for design and [README](../README.md) for usage. Phases are ordered; checkboxes show done vs planned.

**Quick reference:** Phases 1–4 done. Next: PyPI publish (0.2.0), then Phase 5 (DX/tooling) and Phase 6 (extensions).

---

## Current status

- **Core:** Package layout, `FakerType` base, 26 semantic types (person, geo, internet, commerce, date/time, text, phone, finance), tests, and examples.
- **Optional Pydantic:** Works without Pydantic (dataclasses, attrs, etc.); Pydantic schema support when `capper[pydantic]` is installed.
- **Progress:** Phase 1 and 2 complete. Phase 3 packaging done except PyPI publish.

*Recent: Pydantic made optional; README dataclass example.*

---

## Phase 1 — MVP

- [x] Implement `FakerType` base class with automatic Polyfactory registration.
- [x] Implement initial set of core semantic types (person, geo, internet, commerce, date/time).
- [x] Expand to 15–20 core semantic types as needed.
- [x] Unit tests for types and Polyfactory integration.

---

## Phase 2 — Full coverage

- [x] Add remaining Faker providers (Commerce, Text, Date/Time, Phone, Credit cards).
- [x] Ensure all types auto-register on import.
- [x] Align type names and providers with Faker's API across locales where relevant.

---

## Phase 3 — Packaging

- [x] `pyproject.toml` with Faker and Polyfactory; Pydantic optional via `capper[pydantic]`.
- [x] Publish to PyPI (workflow and docs in place; create release to trigger upload).
- [x] Usage examples in repo (e.g. `capper/examples/user_factory.py`).

---

## Phase 4 — Optional enhancements

- [x] Support Faker provider kwargs (e.g. min/max lengths, locales).
- [x] Auto-sync or compatibility notes with new Faker releases.
- [x] (Future) Hypothesis strategies, custom type registration, optional CLI — custom types documented in README; Hypothesis/CLI deferred.

---

## Phase 5 — Developer experience & tooling

- [ ] Hypothesis strategies for capper types (e.g. `capper.strategies.name()`) for property-based tests.
- [ ] Optional CLI (e.g. `capper generate Name Email --count 5`) for ad-hoc fake data from the shell.
- [ ] Ruff and mypy in CI and in `pyproject.toml` (README already badges them).
- [ ] API reference or improved docstrings for IDE/docs.

---

## Phase 6 — Extensions & ecosystem

- [ ] Additional semantic types from Faker (e.g. file paths, UUID, hex color, barcode, or locale helpers).
- [ ] Document or support using a custom Faker instance (e.g. locale-specific) with Polyfactory.
- [ ] Contributing guide or pattern for third-party “capper type packs” (custom FakerType bundles).

---

## Milestones / releases

| Version | Focus |
|--------|--------|
| 0.1.0  | Initial structure, 17 semantic types, optional Pydantic, multi-backend (Pydantic, dataclasses, attrs), tests, examples. |
| 0.2.0  | Phase 2 coverage (26 types: text, phone, finance), auto-registration, provider docs (current). |
| 0.3.0+ | Phase 4 enhancements as needed. |
| 0.4.0  | Phase 5: Hypothesis strategies, optional CLI, Ruff/mypy in CI, API docs. |
| 0.5.0+ | Phase 6: More types, custom Faker/locale support, contrib/plugin story. |

---

*Last updated: 2025-02-24 (added Phase 5 and Phase 6).*

---

*See also: [Package plan](capper_package_plan.md) · [README](../README.md) · [Faker providers](FAKER_PROVIDERS.md)*
