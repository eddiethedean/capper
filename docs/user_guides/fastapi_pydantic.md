## FastAPI and Pydantic tests with Capper

This guide shows how to use Capper types and Polyfactory’s `ModelFactory` in **FastAPI-style** tests.
You do **not** need FastAPI installed to run the companion example script; FastAPI usage is shown as optional snippets.

### Scenario: testing a user API

Define a Pydantic model with Capper types and use a factory for realistic payloads:

```python
from pydantic import BaseModel
from capper import Email, Name
from polyfactory.factories.pydantic_factory import ModelFactory


class UserCreate(BaseModel):
    name: Name
    email: Email


class UserFactory(ModelFactory[UserCreate]):
    """Factory for request/response payloads in tests."""
    __random_seed__ = 42
```

In tests, you can build one payload or a batch:

```python
def test_create_user_payload_shape() -> None:
    payload = UserFactory.build().model_dump()
    assert "name" in payload and "email" in payload
    assert isinstance(payload["name"], str)
    assert isinstance(payload["email"], str)
```

### Optional: wiring into FastAPI tests

With FastAPI installed, you can plug the same factory into route tests:

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/users")
def create_user(user: UserCreate) -> UserCreate:
    # Your real app would save to a database here
    return user


client = TestClient(app)


def test_create_user_route() -> None:
    payload = UserFactory.build().model_dump()
    response = client.post("/users", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == payload["name"]
    assert body["email"] == payload["email"]
```

This pattern keeps Capper usage focused on generating request/response data; you can use the same factory across unit, integration, and contract tests.

### Running the example

From the repo root (with Capper installed):

```bash
python docs/examples/fastapi_pydantic.py
```

The example script prints sample `UserCreate` payloads without requiring FastAPI itself.

Example output (values will vary):

```text
--- Single payload ---
{'name': 'Allison Hill', 'email': 'donaldgarcia@example.net'}

--- Batch of 3 ---
{'name': 'Angie Henderson', 'email': 'davisjesse@example.net'}
{'name': 'Cristian Santos', 'email': 'lrobinson@example.com'}
{'name': 'Abigail Shaffer', 'email': 'jpeterson@example.org'}
```

See also:

- [Getting started](getting_started.md)
- [Models and factories](models_and_factories.md)
- [Reproducible data](reproducible_data.md)
