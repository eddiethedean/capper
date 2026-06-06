# Capper tests

- **test_types.py** — ModelFactory build for all exported FakerTypes; HexColor kwargs; seed and use_faker reproducibility.
- **test_polyfactory_integration.py** — Pydantic ModelFactory and DataclassFactory; shared Faker; faker_field overrides; Pydantic coercion.
- **test_faker_field.py** — faker_field kwargs merging and seed reproducibility.
- **test_registry.py** — build_type_registry unit tests and capper export completeness.
- **test_edge_cases.py** — Version fallback, registration/strategy/faker_field error paths, locale and use_faker edge cases.
- **test_cli.py** — CLI generate subcommand: output, seed determinism, count edge cases, typo suggestions.
- **test_thread_safety.py** — Per-thread use_faker and seed isolation.
- **test_hypothesis_strategies.py** — Hypothesis st.from_type and for_type (requires capper[hypothesis]).
- **test_docs_examples.py** — Subprocess smoke tests for docs/examples scripts.
- **test_deprecations.py** — Internal warn_deprecated helper.
- **test_bug_fixes.py** — Regression tests for bug-audit fixes (faker_field, CLI TSV, Hypothesis isolation, validation).
- **benchmark_core.py** — Performance benchmarks (deselect with `-m 'not benchmark'`).
