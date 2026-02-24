# Compatibility

Version support and upgrade guidance for Capper. For deprecations, see [Deprecation policy](#deprecation-policy) below.

## Thread safety

The module-level **faker** instance and **use_faker()** are process-wide. Do not call **use_faker()** from multiple threads while other threads are building models; the shared Faker is not thread-safe for switching and concurrent use. Use a single Faker (or call **use_faker()** only once at startup) when using Capper from multiple threads.

## Supported versions

Capper is tested against:

- **Python:** 3.10, 3.11, 3.12 (see [CI matrix](https://github.com/eddiethedean/capper/blob/main/.github/workflows/ci.yml)); minimum supported is **3.10** (Python 3.9 is EOL and no longer supported).
- **Faker:** >= 20.0 (see [pyproject.toml](https://github.com/eddiethedean/capper/blob/main/pyproject.toml) `dependencies`).
- **Polyfactory:** >= 2.0.

Optional extras (Pydantic, Hypothesis) have their own version constraints in `pyproject.toml`.

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
- **Documentation:** Deprecations are listed in [CHANGELOG.md](https://github.com/eddiethedean/capper/blob/main/CHANGELOG.md) under "Deprecated" and in release notes. Where practical, code uses `warnings.warn(..., DeprecationWarning)`.
- **Removal:** After the deprecation period, a following minor or major release may remove or change the behavior.

See [CONTRIBUTING.md](https://github.com/eddiethedean/capper/blob/main/CONTRIBUTING.md) for release steps.
