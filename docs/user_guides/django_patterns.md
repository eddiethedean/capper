## Django-style patterns with Capper data

Capper does not depend on Django, but you can still use Capper types and Polyfactory factories alongside Django models and services.
This guide focuses on **patterns** rather than a full Django project inside this repo.

### Service-layer pattern with Pydantic schemas

A common approach is to keep Django models thin and use Pydantic schemas plus factories for test data.

```python
from pydantic import BaseModel
from capper import Email, Name
from polyfactory.factories.pydantic_factory import ModelFactory


class UserSchema(BaseModel):
    name: Name
    email: Email


class UserSchemaFactory(ModelFactory[UserSchema]):
    __random_seed__ = 123
```

In a Django test module you can convert the schema into a Django model instance:

```python
from myapp.models import User  # Django model


def test_creates_user_from_schema(db) -> None:
    schema = UserSchemaFactory.build()
    user = User.objects.create(name=schema.name, email=schema.email)
    assert user.pk is not None
```

This keeps Capper and Polyfactory on the **schema side**, avoiding tight coupling to Django internals while still getting realistic data.

### Using Capper with Django REST Framework serializers

You can also pass Capper-backed schemas into serializers:

```python
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()


def test_user_serializer_round_trip() -> None:
    schema = UserSchemaFactory.build()
    serializer = UserSerializer(data=schema.model_dump())
    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["email"] == schema.email
```

### Running the example

From the repo root (with Capper installed):

```bash
python docs/examples/django_patterns.py
```

The example script mirrors the schema/factory patterns without importing Django itself.

Example output (values will vary):

```text
UserSchema: {'name': 'Brandon Russell', 'email': 'robersonnancy@example.com'}

--- Batch ---
{'name': 'Evelyn Christian', 'email': 'derekhoffman@example.net'}
{'name': 'Aaron Graham', 'email': 'johnsnicholas@example.org'}
```

For real projects, drop the same schemas and factories into your `tests/` directory.

See also:

- [Models and factories](models_and_factories.md)
- [Custom types](custom_types.md)
- [Extending Capper](../extending.md)
