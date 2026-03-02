# Capper roadmap

High-level development phases and current status. See [capper_package_plan.md](capper_package_plan.md) for design and [README](../README.md) for usage. Phases are ordered; checkboxes show done vs planned.

**Quick reference:** Phases 1–9 done. Current: 0.3.0 (Phase 9 — reliability, performance, coverage).

---

## Current status

- **Core:** Package layout, `FakerType` base, 33 semantic types (person, geo, internet, commerce, date/time, text, phone, finance, file, misc, color, barcode), tests, and examples.
- **Optional Pydantic:** Works without Pydantic (dataclasses, attrs, etc.); Pydantic schema support when `capper[pydantic]` is installed.
- **Progress:** Phases 1–9 complete (Phase 9: benchmarks, CI performance gate, coverage ≥98%, edge-case tests).

*Recent: Phase 9 — benchmarks and baseline (docs/benchmarks.md), coverage gate (--cov-fail-under=98), performance test (1000 builds &lt;30s), edge-case tests (seeding, use_faker/locale, registration failures).*

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

## Phase 9 — Reliability, performance, and coverage

- [x] Benchmark core flows (Pydantic models, dataclasses, Hypothesis strategies, CLI) and publish baseline numbers. **Done:** `pytest capper/tests/benchmark_core.py --benchmark-only`, baseline in [benchmarks.md](benchmarks.md).
- [x] Add lightweight performance regression checks in CI (e.g. “no >X% slowdown” for key benchmarks or representative tests). **Done:** 1000× `UserFactory.build()` must complete in &lt;30s (Option B timing test).
- [x] Raise and hold coverage targets (e.g. ≥ 98–99% for `capper/`) and keep `--cov-report=term-missing` as a release gate. **Done:** CI runs with `--cov-fail-under=98`; library coverage ≥98%.
- [x] Add targeted tests for edge cases around seeding, `use_faker()`, locales, and Hypothesis registration failures. **Done:** [test_edge_cases.py](../capper/tests/test_edge_cases.py) (version fallback, use_faker(None) in fresh thread, invalid/non-callable provider, strategies errors, locale de_DE).
- [x] Document known limitations and recommended patterns for multi-threaded use. **Done:** Capper is now thread-safe (per-thread Faker via proxy); see [compatibility](compatibility.md#thread-safety) and [reproducible data](user_guides/reproducible_data.md).

---

## Phase 10 — API stability and versioning

- [ ] Define the “public API surface” explicitly (what is guaranteed vs. internal) and document it in the API reference.
- [ ] Tighten or add deprecation warnings for any APIs that may change before 1.0.0.
- [ ] Document a clear semantic-versioning policy for Capper (what counts as breaking vs. minor vs. patch).
- [ ] Audit type names, behaviors, and error messages for consistency before declaring them stable.
- [ ] Add a short “Upgrading between minor versions” section with concrete examples (especially around Faker/Polyfactory upgrades).

---

## Phase 11 — Ecosystem, integrations, and UX

- [ ] Add deeper usage guides and examples for common stacks (e.g. FastAPI/Pydantic, Django + Pydantic, dataclasses/attrs-heavy codebases).
- [ ] Provide small “starter templates” or snippets for typical test setups (pytest fixtures, factory modules, Hypothesis strategies).
- [ ] Document patterns for organizing large projects that rely heavily on Capper types (naming conventions, module layout).
- [ ] Polish CLI UX (help text, error messages, discoverability) based on real-world feedback.
- [ ] Highlight and document third-party “capper type packs” or integrations (if/when they exist) in the docs.

---

## Phase 12 — Production-ready 1.0 and long-term maintenance

- [ ] Cut a 1.0.0 release once Phase 9–11 items are complete and the API surface is stable.
- [ ] Establish a support and maintenance policy (e.g. supported Python and dependency versions, backport scope).
- [ ] Add or refine project governance docs (issue and PR templates, code of conduct, release checklist).
- [ ] Monitor and respond to bug reports around Faker and Polyfactory upstream changes; document any needed workarounds.
- [ ] Periodically review docs, examples, and CI to ensure they stay aligned with real-world usage and current best practices.

---

## Milestones / releases

| Version | Focus |
|--------|--------|
| 0.1.0  | Initial structure, 17 semantic types, optional Pydantic, multi-backend, tests, examples. |
| 0.2.0  | 26 types, Phase 5 (Hypothesis strategies, CLI, Ruff/mypy in CI, docstrings), user guides, notebooks. |
| 0.3.0  | Phase 8: Compatibility doc, deprecation policy, Python 3.10+ minimum (dropped 3.9). **Current.** |
| 0.4.0  | Ship remaining Phase 6/7 content (33 types, `use_faker()`, CONTRIBUTING, API reference, CHANGELOG, etc.); tighten CI and docs around them. |
| 0.5.0  | Phase 9 focus: reliability, performance baselines, stricter coverage and CI gating. |
| 1.0.0  | Phases 10–12: explicit public API, versioning policy, ecosystem docs, and a production-ready, stable release. |

---

*Last updated: 2026-03-02 (Phase 9 complete).*

---

*See also: [Package plan](capper_package_plan.md) · [README](../README.md) · [Faker providers](FAKER_PROVIDERS.md)*
