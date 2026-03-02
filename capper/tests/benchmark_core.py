"""Performance benchmarks for core flows (ModelFactory, DataclassFactory, Hypothesis strategy).

Run with: pytest capper/tests/benchmark_core.py -v --benchmark-only
Exclude from default test run: pytest -m 'not benchmark'
"""

from dataclasses import dataclass

import pytest

from capper import Email, Name


@pytest.mark.benchmark
def test_bench_model_factory_build(benchmark: object) -> None:
    """Benchmark ModelFactory.build() with 2 Capper types (Name, Email)."""
    from polyfactory.factories.pydantic_factory import ModelFactory
    from pydantic import BaseModel

    class User(BaseModel):
        name: Name
        email: Email

    class UserFactory(ModelFactory[User]):
        pass

    benchmark(UserFactory.build)


@pytest.mark.benchmark
def test_bench_dataclass_factory_build(benchmark: object) -> None:
    """Benchmark DataclassFactory.build() with 2 Capper types (Name, Email)."""
    from polyfactory.factories import DataclassFactory

    @dataclass
    class Person:
        name: Name
        email: Email

    class PersonFactory(DataclassFactory[Person]):
        pass

    benchmark(PersonFactory.build)


@pytest.mark.benchmark
def test_bench_hypothesis_strategy_example(benchmark: object) -> None:
    """Benchmark drawing one value from st.from_type(Name) via strategy.example()."""
    from capper import strategies

    strategy = strategies.for_type(Name)

    def draw_one() -> None:
        strategy.example()

    benchmark(draw_one)
