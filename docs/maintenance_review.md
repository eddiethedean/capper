# Maintenance review checklist

This checklist is intended for periodic hygiene reviews (for example, once per minor release or quarterly) to keep Capper aligned with real-world usage.

## Docs and examples

- Run all example scripts in `docs/examples/` and ensure they still execute successfully against the latest released version.
- Scan `docs/user_guides/` and `README.md` for:
  - Stale API examples (renamed functions, types, or CLI flags).
  - Hard-coded version numbers that no longer match the current release.
- Review `docs/extending.md`:
  - Confirm the “Known type packs and integrations” section is up to date.
  - Remove or update links that are no longer maintained if needed.
- Check `docs/ROADMAP.md`:
  - Ensure status checkboxes and milestones match actual released versions.
  - Update “Current status” and “Current release” as needed.

## CI and tooling

- Review `.github/workflows/ci.yml` and `.github/workflows/publish.yml`:
  - Confirm Python versions match the supported versions in `docs/compatibility.md`.
  - Look for deprecated GitHub Actions or configuration patterns and update if needed.
- Evaluate coverage and performance gates:
  - Confirm `--cov-fail-under` is still appropriate.
  - Confirm any timing-based tests or benchmarks are still stable and informative.
- Ensure `pyproject.toml` tooling sections (Ruff, mypy, etc.) are consistent with what CI runs.

## Compatibility and support policy

- Revisit `docs/compatibility.md`:
  - Update supported Python/Faker/Polyfactory versions as upstream projects evolve.
  - Adjust backport policy notes if support horizons change.

## Outcomes

- Open issues or pull requests for any fixes or improvements discovered during the review.
- Optionally note the date of the last maintenance review in `docs/ROADMAP.md` or a project board.

