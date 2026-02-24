# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Compatibility doc ([docs/compatibility.md](docs/compatibility.md)) with version ranges, upgrade guidance, and deprecation policy.
- Phase 8: compatibility docs, deprecation policy, Python 3.10+ minimum.

### Removed

- Dropped support for Python 3.9 (EOL). Minimum is now 3.10.

## [0.4.0] - 2026-02-24

### Added

- 33 semantic types: added File (`FilePath`, `FileName`, `FileExtension`), Misc (`UUID`), Color (`HexColor`), Barcode (`EAN13`, `EAN8`).
- `use_faker(instance)` to set a custom Faker instance for both Capper and Polyfactory (e.g. locale-specific).
- Documentation for locales and custom Faker in user guide (reproducible_data.md).
- CONTRIBUTING.md with dev setup and how to add new built-in types.
- docs/extending.md describing third-party type packs pattern.

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

[Unreleased]: https://github.com/eddiethedean/capper/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/eddiethedean/capper/compare/v0.2.0...v0.4.0
[0.2.0]: https://github.com/eddiethedean/capper/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/eddiethedean/capper/releases/tag/v0.1.0
