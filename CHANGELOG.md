# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_No unreleased changes yet._

## [0.4.1] - 2026-03-02

### Added

- **Deprecation helper:** Added internal `capper._deprecations.warn_deprecated(...)` to emit consistent `DeprecationWarning` messages and support a clear deprecation policy.

## [0.4.0] - 2026-03-02

### Added

- **Thread-safe per-thread Faker:** Each thread now has its own Faker instance. The module-level `faker` is a proxy that forwards to the current thread's Faker; `seed(n)` and `use_faker(instance)` only affect the current thread. No API changes; safe for concurrent use from multiple threads. See [compatibility](docs/compatibility.md#thread-safety).
- **Reliability and coverage gate (Phase 9):** Required coverage ≥ 98% for the `capper/` package, enforced in CI with `--cov-report=term-missing` and `--cov-fail-under=98`; added targeted edge-case tests for seeding, `use_faker()`, locales, and Hypothesis registration failures.
- **Benchmarks and performance checks:** Added `capper/tests/benchmark_core.py` with pytest-benchmark and documented baseline timings in `docs/benchmarks.md`; added a lightweight performance test (1000× `UserFactory.build()` under a generous threshold) that runs in CI.
- **CI and docs improvements:** CI now runs Ruff, mypy, tests (with coverage gate) and a strict MkDocs build on all supported Python versions; docs were updated to reflect Phase 9 completion and to fix strict MkDocs warnings.

## [0.3.0] - 2026-02-24

### Added

- Compatibility doc ([docs/compatibility.md](docs/compatibility.md)) with version ranges, upgrade guidance, and deprecation policy.
- Phase 8: compatibility docs, deprecation policy, Python 3.10+ minimum.

### Removed

- Dropped support for Python 3.9 (EOL). Minimum is now 3.10.

## [0.2.0]

### Added

- 26 semantic types; Hypothesis strategies (`st.from_type()`, `capper.strategies.for_type()`); CLI (`capper generate Name Email --count 5`).
- Ruff and mypy in CI and pyproject.toml; improved docstrings.
- User guides (getting started, models and factories, reproducible data, custom types) and example notebooks.

## [0.1.0]

### Added

- Initial package structure; `FakerType` base class with automatic Polyfactory registration.
- 17 semantic types (person, geo, internet, commerce, date/time).
- Optional Pydantic support; multi-backend (Pydantic, dataclasses, attrs).
- Unit tests and usage examples.

[Unreleased]: https://github.com/eddiethedean/capper/compare/v0.4.1...HEAD
[0.4.1]: https://github.com/eddiethedean/capper/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/eddiethedean/capper/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/eddiethedean/capper/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/eddiethedean/capper/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/eddiethedean/capper/releases/tag/v0.1.0
