# Compatibility

Version support and upgrade guidance for Capper. For deprecations, see [Deprecation policy](#deprecation-policy) below.

## Thread safety

Capper is **thread-safe**: each thread has its own Faker instance. The module-level **faker** is a proxy that forwards to the current thread's Faker. **`seed(n)`** and **`use_faker(instance)`** only affect the current thread, so you can safely call them from multiple threads or use different locales per thread. Polyfactory's factory builds use the same per-thread Faker.

## Supported versions

Capper 0.5.x and 1.0.x are tested against:

- **Python:** 3.10, 3.11, 3.12, 3.13 (see [CI matrix](https://github.com/eddiethedean/capper/blob/main/.github/workflows/ci.yml)); minimum supported is **3.10** (Python 3.9 is EOL and no longer supported).
- **Faker:** >= 20.0 (see [pyproject.toml](https://github.com/eddiethedean/capper/blob/main/pyproject.toml) `dependencies`).
- **Polyfactory:** >= 2.0.

Optional extras (Pydantic, Hypothesis) have their own version constraints in `pyproject.toml`.

### Backwards-compatibility and backports

- **Stable line:** For Capper 1.0.x, we aim to keep the documented public API stable; breaking changes will only ship in a future 2.0.0.
- **Backports:** Critical bug fixes (including compatibility fixes for supported Python/Faker/Polyfactory versions) may be backported to the latest 1.0.x release.
- **What is _not_ backported:** New features, new semantic types, and non-trivial behavior changes generally land in new minor releases rather than patch releases.

## Upgrading Faker

Major Faker releases can rename or change provider methods. If a Capper type fails after upgrading Faker:

1. Check [Faker's changelog](https://faker.readthedocs.io/en/stable/changelog.html) for provider or method changes.
2. Check [FAKER_PROVIDERS.md](FAKER_PROVIDERS.md) to see which Faker method the type uses.
3. Update the type's `faker_provider` (or add a new type) if the method name or behavior changed; consider opening a PR.
4. As a workaround, you can pin Faker to a known-good version in your environment.

## Upgrading Polyfactory

Capper uses `BaseFactory.__faker__` and `BaseFactory.add_provider()`. If Polyfactory changes that API in a major release, Capper may need a release to stay compatible. Check this repo and [CHANGELOG.md](https://github.com/eddiethedean/capper/blob/main/CHANGELOG.md) for compatibility notes when upgrading Polyfactory.

## Deprecation policy

- **Advance notice:** Deprecated features or breaking changes are announced at least **one minor release** in advance (e.g. deprecation in 0.6.0, removal in 0.7.0).
- **Documentation:** Deprecations are listed in [CHANGELOG.md](https://github.com/eddiethedean/capper/blob/main/CHANGELOG.md) under \"Deprecated\" and in release notes. Where practical, code uses the internal helper `capper._deprecations.warn_deprecated(...)` to emit `DeprecationWarning`.
- **Removal:** After the deprecation period, a following minor or major release may remove or change the behavior.

Example:

```python
from capper._deprecations import warn_deprecated


def old_api() -> None:
    warn_deprecated(
        \"capper.old_api\",
        removal_version=\"0.6.0\",
        alternative=\"capper.new_api\",
    )
    ...
```

## Versioning and releases

Capper follows [Semantic Versioning](https://semver.org/) and uses the following guidelines:

- **Major (1.y.z)** — Breaking changes to the documented public API surface (e.g. removing types or functions from `capper`, changing behavior or error types in incompatible ways).
- **Minor (0.x.0 / 1.x.0)** — Backwards-compatible feature work: new semantic types, new CLI options, additional docs, performance improvements, and new integrations.
- **Patch (x.y.z)** — Backwards-compatible bug fixes, small behavior corrections that do not break documented contracts, and docs-only changes.

### Upgrading between minor versions

When upgrading between minor versions (e.g. from 0.4 to 0.5):

- Check the [CHANGELOG.md](https://github.com/eddiethedean/capper/blob/main/CHANGELOG.md) for any **Deprecated** items and their suggested replacements.
- Look for notes about **tightened validation** or **clearer error messages**; if your tests assert on exact strings, you may need to update expected messages while keeping the behavior the same.
- If an API you depend on is marked as deprecated, migrate to the recommended alternative before the documented removal version (e.g. switch from `capper.old_api` to `capper.new_api` in the example above).

See [CONTRIBUTING.md](https://github.com/eddiethedean/capper/blob/main/CONTRIBUTING.md) for release steps.
