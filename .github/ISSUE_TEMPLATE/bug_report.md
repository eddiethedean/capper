---
name: Bug report
about: Create a report to help us improve Capper
labels: bug
---

## Summary

Describe the bug and what you expected to happen.

## Environment

- Capper version: (e.g. 0.5.0)
- Python version: (e.g. 3.11.8)
- Faker version:
- Polyfactory version:
- OS:

## Reproduction

Please provide a minimal, self-contained example if possible. For example:

```python
from capper import Name
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import BaseModel


class User(BaseModel):
    name: Name


class UserFactory(ModelFactory[User]):
    pass


user = UserFactory.build()
print(user)
```

Include:

- Exact commands you ran (e.g. pytest invocation, CLI usage).
- Full traceback or error messages.

## Additional context

Add any other context, logs, or configuration that might help diagnose the issue.

