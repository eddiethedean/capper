# API Reference

Programmatic API for Capper: the main package, the shared Faker instance, and the base type.

## Package: capper

Top-level exports: semantic types (`Name`, `Email`, etc.), `FakerType`, `faker`, `seed`, and `use_faker`. Import with `from capper import Name, Email, seed`.

::: capper

## Base: FakerType, faker, seed, use_faker

The base class and shared Faker instance. Use `seed(n)` for reproducibility; use `use_faker(instance)` to switch to a custom Faker (e.g. locale-specific).

::: capper.base.FakerType
::: capper.base.faker
::: capper.base.seed
::: capper.base.use_faker

## Semantic types

All semantic types are subclasses of `FakerType` and are used as type annotations in your models. For the full list and the Faker provider used by each, see [Faker providers](FAKER_PROVIDERS.md).

Categories: **Person** (`Name`, `FirstName`, `LastName`, `Job`), **Geo** (`Address`, `City`, `Country`), **Internet** (`Email`, `URL`, `IP`, `UserName`), **Commerce** (`Company`, `Product`, `Currency`, `Price`), **Date/time** (`Date`, `DateTime`, `Time`), **Text** (`Paragraph`, `Sentence`), **Phone** (`PhoneNumber`, `CountryCallingCode`), **Finance** (`CreditCardNumber`, `CreditCardExpiry`, `CreditCardProvider`), **File** (`FilePath`, `FileName`, `FileExtension`), **Misc** (`UUID`), **Color** (`HexColor`), **Barcode** (`EAN13`, `EAN8`).
