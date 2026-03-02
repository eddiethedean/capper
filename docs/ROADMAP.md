# Capper roadmap

High-level development phases and current status. See [capper_package_plan.md](capper_package_plan.md) for design and [README](README.md) for usage. Phases are ordered; checkboxes show done vs planned.

**Quick reference:** Phases 1–11 done. Current release: 0.5.0 (Phase 11 — ecosystem docs and UX); 1.0.0 (Phase 12) will finalize support policy and long-term maintenance.

---

## Current status

- **Core:** Package layout, `FakerType` base, 33 semantic types (person, geo, internet, commerce, date/time, text, phone, finance, file, misc, color, barcode), tests, and examples.
- **Optional Pydantic:** Works without Pydantic (dataclasses, attrs, etc.); Pydantic schema support when `capper[pydantic]` is installed.
- **Progress:** Phases 1–11 complete (Phase 10: public API definition, deprecation helper, versioning and upgrade guidance; Phase 11: ecosystem docs, guides, and CLI UX polish).

*Recent: Phase 11 — new ecosystem/user guides (FastAPI, Django patterns, dataclasses/attrs, test templates, project structure), improved CLI UX, and updated docs navigation.*

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
- [x] Add targeted tests for edge cases around seeding, `use_faker()`, locales, and Hypothesis registration failures. **Done:** `capper/tests/test_edge_cases.py` (version fallback, use_faker(None) in fresh thread, invalid/non-callable provider, strategies errors, locale de_DE).
- [x] Document known limitations and recommended patterns for multi-threaded use. **Done:** Capper is now thread-safe (per-thread Faker via proxy); see [compatibility](compatibility.md#thread-safety) and [reproducible data](user_guides/reproducible_data.md).

---

## Phase 10 — API stability and versioning

- [x] Define the “public API surface” explicitly (what is guaranteed vs. internal) and document it in the API reference. **Done:** See [API reference](api.md) “Public API surface”.
- [x] Tighten or add deprecation warnings for any APIs that may change before 1.0.0. **Done:** Added internal helper `capper._deprecations.warn_deprecated(...)` and documented policy in [compatibility](compatibility.md).
- [x] Document a clear semantic-versioning policy for Capper (what counts as breaking vs. minor vs. patch). **Done:** See [compatibility](compatibility.md#versioning-and-releases).
- [x] Audit type names, behaviors, and error messages for consistency before declaring them stable. **Done:** Error paths are standardized and covered by tests; see `capper/tests/test_edge_cases.py`, `capper/tests/test_cli.py`, and `capper/tests/test_hypothesis_strategies.py`.
- [x] Add a short “Upgrading between minor versions” section with concrete examples (especially around Faker/Polyfactory upgrades). **Done:** See [compatibility](compatibility.md#upgrading-between-minor-versions).

---

## Phase 11 — Ecosystem, integrations, and UX

- [x] Add deeper usage guides and examples for common stacks (e.g. FastAPI/Pydantic, Django + Pydantic, dataclasses/attrs-heavy codebases). **Done:** See `docs/user_guides/fastapi_pydantic.md`, `django_patterns.md`, and `dataclasses_and_attrs.md` (each with runnable examples in `docs/examples/`).
- [x] Provide small “starter templates” or snippets for typical test setups (pytest fixtures, factory modules, Hypothesis strategies). **Done:** See `docs/user_guides/test_setup_templates.md` and `docs/examples/test_setup_templates.py`.
- [x] Document patterns for organizing large projects that rely heavily on Capper types (naming conventions, module layout). **Done:** See `docs/user_guides/project_structure.md`.
- [x] Polish CLI UX (help text, error messages, discoverability) based on real-world feedback. **Done:** Improved help/epilog and unknown-type suggestions in `capper/cli.py`, with tests in `capper/tests/test_cli.py`.
- [x] Highlight and document third-party “capper type packs” or integrations (if/when they exist) in the docs. **Done:** See “Known type packs and integrations” in `docs/extending.md`.

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
| 0.3.0  | Phase 8: Compatibility doc, deprecation policy, Python 3.10+ minimum (dropped 3.9). |
| 0.4.0  | Phase 9: reliability, performance baselines, stricter coverage and CI gating. |
| 0.4.1  | Phase 10: public API surface, deprecation helper, and versioning/upgrade guidance. |
| 0.5.0  | Phase 11: ecosystem docs, UX improvements, and broader integrations. **Current release.** |
| 1.0.0  | Phase 12 and beyond: long-term maintenance, governance docs, and a production-ready, stable release. |

---

*Last updated: 2026-03-02 (Phase 11 complete; 0.5.0 unreleased).*

---

*See also: [Package plan](capper_package_plan.md) · [README](README.md) · [Faker providers](FAKER_PROVIDERS.md)*
