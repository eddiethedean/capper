"""Runnable example for the Dataclasses and attrs user guide.

Run from repo root (with capper installed): python docs/examples/dataclasses_and_attrs.py
"""

from dataclasses import dataclass

from polyfactory.factories import DataclassFactory

from capper import Email, Name


@dataclass
class Person:
    name: Name
    email: Email


class PersonFactory(DataclassFactory[Person]):
    __random_seed__ = 7


if __name__ == "__main__":
    print("--- Person (dataclass) ---")
    person = PersonFactory.build()
    print(person)
