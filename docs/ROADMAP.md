# Capper roadmap

High-level development phases and current status. See [capper_package_plan.md](capper_package_plan.md) for design and [README](../README.md) for usage. Phases are ordered; checkboxes show done vs planned.

**Quick reference:** Phases 1–8 done. Current: 0.5.0 (Phase 8 — compatibility & maintenance).

---

## Current status

- **Core:** Package layout, `FakerType` base, 33 semantic types (person, geo, internet, commerce, date/time, text, phone, finance, file, misc, color, barcode), tests, and examples.
- **Optional Pydantic:** Works without Pydantic (dataclasses, attrs, etc.); Pydantic schema support when `capper[pydantic]` is installed.
- **Progress:** Phases 1–8 complete (Phase 8: compatibility doc, deprecation policy, Python 3.10+ minimum).

*Recent: Phase 8 — docs/compatibility.md (version ranges, upgrade guidance, deprecation policy); dropped Python 3.9 (EOL), minimum 3.10.*

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
- [x] Hypothesis strategies (Phase 5), custom types documented in README; optional CLI in Phase 5.

---

## Phase 5 — Developer experience & tooling

- [x] Hypothesis strategies for capper types (e.g. `st.from_type(Name)`, `capper.strategies.for_type()`) for property-based tests.
- [x] Optional CLI (e.g. `capper generate Name Email --count 5`) for ad-hoc fake data from the shell.
- [x] Ruff and mypy in CI and in `pyproject.toml` (README already badges them).
- [x] API reference or improved docstrings for IDE/docs.

---

## Phase 6 — Extensions & ecosystem

- [x] Additional semantic types from Faker (e.g. file paths, UUID, hex color, barcode, or locale helpers).
- [x] Document or support using a custom Faker instance (e.g. locale-specific) with Polyfactory.
- [x] Contributing guide or pattern for third-party “capper type packs” (custom FakerType bundles).

---

## Phase 7 — Documentation & API

- [x] Add API reference (e.g. Sphinx or MkDocs) for public types and `FakerType` / `seed` / `use_faker`.
- [x] Add CHANGELOG (e.g. `CHANGELOG.md` or Keep a Changelog) and update it with each release.
- [x] Cross-link or surface example notebooks from the docs index so they are easy to discover.

---

## Phase 8 — Compatibility & maintenance

- [x] Document supported Faker and Polyfactory version ranges and how to handle upgrades (e.g. in README or docs).
- [x] Define a simple deprecation policy (e.g. one minor version warning before removing or changing behavior).
- [x] Re-evaluate minimum Python version when 3.9 is EOL; update `requires-python` and CI if needed.

---

## Milestones / releases

| Version | Focus |
|--------|--------|
| 0.1.0  | Initial structure, 17 semantic types, optional Pydantic, multi-backend, tests, examples. |
| 0.2.0  | 26 types, Phase 5 (Hypothesis strategies, CLI, Ruff/mypy in CI, docstrings), user guides, notebooks. |
| 0.3.0+ | Phase 4 enhancements as needed. |
| 0.4.0  | Phase 6: 33 types (file, UUID, HexColor, EAN13/EAN8), use_faker(), locale docs, CONTRIBUTING.md, type-packs (extending.md). **Current.** |
| 0.5.0  | Phase 7: API reference (MkDocs + mkdocstrings), CHANGELOG.md, notebook links in docs. |
| 0.6.0  | Phase 8: Compatibility doc, deprecation policy, Python 3.10+ minimum (dropped 3.9). |

---

*Last updated: 2026-02-24 (Phase 8 complete).*

---

*See also: [Package plan](capper_package_plan.md) · [README](../README.md) · [Faker providers](FAKER_PROVIDERS.md)*
