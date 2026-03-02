# API Reference

Programmatic API for Capper: the main package, the shared Faker instance, and the base type.

## Public API surface

Capper’s public API (stable pre-1.0) consists of:

- **Modules**
  - `capper` — semantic types, Faker proxy, and helpers.
  - `capper.strategies` — Hypothesis integration (`for_type` and `st.from_type(...)` once imported).
- **Objects**
  - Semantic types imported from `capper` (e.g. `Name`, `Email`, `Address`, `Price`, `UUID`, `EAN13`).
  - `FakerType`, `faker`, `seed`, `use_faker` from `capper`.
  - `for_type` from `capper.strategies`.

Internal helpers and modules not listed here may change between releases.

## Package: capper

Top-level exports: semantic types (`Name`, `Email`, etc.), `FakerType`, `faker`, `seed`, and `use_faker`. Import with `from capper import Name, Email, seed`.

::: capper

## Base: FakerType, faker, seed, use_faker

The base class and shared per-thread Faker instance. Use `seed(n)` for reproducibility; use `use_faker(instance)` to switch to a custom Faker (e.g. locale-specific) for the current thread.

::: capper.base.FakerType
::: capper.base.faker
::: capper.base.seed
::: capper.base.use_faker

## Semantic types

All semantic types are subclasses of `FakerType` and are used as type annotations in your models. For the full list and the Faker provider used by each, see [Faker providers](FAKER_PROVIDERS.md).

Categories: **Person** (`Name`, `FirstName`, `LastName`, `Job`), **Geo** (`Address`, `City`, `Country`), **Internet** (`Email`, `URL`, `IP`, `UserName`), **Commerce** (`Company`, `Product`, `Currency`, `Price`), **Date/time** (`Date`, `DateTime`, `Time`), **Text** (`Paragraph`, `Sentence`), **Phone** (`PhoneNumber`, `CountryCallingCode`), **Finance** (`CreditCardNumber`, `CreditCardExpiry`, `CreditCardProvider`), **File** (`FilePath`, `FileName`, `FileExtension`), **Misc** (`UUID`), **Color** (`HexColor`), **Barcode** (`EAN13`, `EAN8`).
