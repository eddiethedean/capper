# Benchmarks

Performance baseline for core flows. Regressions can be checked in CI with a timing gate (see Phase 9).

## Command

```bash
pytest capper/tests/benchmark_core.py -v --benchmark-only
```

Benchmarks are marked with `@pytest.mark.benchmark` and are excluded from the default test run (`pytest -m 'not benchmark'`).

## Baseline (reference)

Run on a typical developer machine (Darwin, Python 3.11). Your numbers will vary.

| Test | Mean (μs) | OPS (Kops/s) |
|------|-----------|--------------|
| ModelFactory.build() (Name, Email) | ~237 | ~4.2 |
| DataclassFactory.build() (Name, Email) | ~166 | ~6.0 |
| Hypothesis strategy.example() for Name | ~347 | ~2.9 |

- **ModelFactory:** Pydantic model with 2 Capper types; one `.build()` per iteration.
- **DataclassFactory:** Dataclass with 2 Capper types; one `.build()` per iteration.
- **Hypothesis:** One draw from `st.from_type(Name)` via `.example()` per iteration.

CI uses a lightweight performance check (e.g. 1000× `UserFactory.build()` in under a threshold) rather than comparing to this baseline; this document is for manual regression checks and reference.
