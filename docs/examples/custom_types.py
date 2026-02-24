"""Runnable example for the Custom types user guide.

Run from repo root (with capper installed): python docs/examples/custom_types.py
"""

from capper.base import FakerType
from pydantic import BaseModel
from polyfactory.factories.pydantic_factory import ModelFactory


# faker_kwargs: constrain existing provider
class ShortSentence(FakerType):
    faker_provider = "sentence"
    faker_kwargs = {"nb_words": 5}


# New type: faker_provider only
class CompanyName(FakerType):
    faker_provider = "company"


# Provider + kwargs
class USDate(FakerType):
    faker_provider = "date"
    faker_kwargs = {"pattern": "%m/%d/%Y"}


class Snippet(BaseModel):
    title: str
    summary: ShortSentence


class SnippetFactory(ModelFactory[Snippet]):
    pass


class Startup(BaseModel):
    name: CompanyName
    slogan: ShortSentence


class StartupFactory(ModelFactory[Startup]):
    pass


class Event(BaseModel):
    name: str
    date: USDate


class EventFactory(ModelFactory[Event]):
    pass


if __name__ == "__main__":
    print("--- ShortSentence (faker_kwargs) ---")
    s = SnippetFactory.build()
    print("Summary (5 words):", s.summary)

    print("\n--- CompanyName + ShortSentence ---")
    startup = StartupFactory.build()
    print(startup.name, "—", startup.slogan)

    print("\n--- USDate (provider + kwargs) ---")
    e = EventFactory.build()
    print(e.name, e.date)
