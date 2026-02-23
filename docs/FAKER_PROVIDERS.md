# Faker provider mapping

Each capper type uses a single [Faker](https://faker.readthedocs.io/) provider method. Behavior may vary by locale (e.g. `Faker('de_DE')` vs default).

| Capper type | Faker provider |
|-------------|-----------------|
| **Person** | |
| Name | `name` |
| FirstName | `first_name` |
| LastName | `last_name` |
| Job | `job` |
| **Geo** | |
| Address | `address` |
| City | `city` |
| Country | `country` |
| **Internet** | |
| Email | `email` |
| URL | `url` |
| IP | `ipv4` |
| UserName | `user_name` |
| **Commerce** | |
| Company | `company` |
| Product | `catch_phrase` |
| Currency | `currency_code` |
| Price | `pricetag` |
| **Date/time** | |
| Date | `date` |
| DateTime | `iso8601` |
| Time | `time` |
| **Text** | |
| Paragraph | `paragraph` |
| Sentence | `sentence` |
| **Phone** | |
| PhoneNumber | `phone_number` |
| CountryCallingCode | `country_calling_code` |
| **Finance** | |
| CreditCardNumber | `credit_card_number` |
| CreditCardExpiry | `credit_card_expire` |
| CreditCardProvider | `credit_card_provider` |
