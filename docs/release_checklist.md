# Release checklist

This checklist is for maintainers cutting a new Capper release (including 1.0.0 and future 1.x versions).

1. **Verify CI is green on `main`**
   - Ensure the latest commits on `main` pass the CI workflow in `.github/workflows/ci.yml`.

2. **Update `CHANGELOG.md`**
   - Move entries from **[Unreleased]** into a new `## [X.Y.Z] - YYYY-MM-DD` section.
   - Summarize noteworthy changes (features, fixes, deprecations).

3. **Update version metadata**
   - Bump the version in `pyproject.toml` under `[project].version`.
   - Update the fallback `__version__` in `capper/__init__.py` if necessary.

4. **Check docs and README**
   - Ensure `README.md` and `docs/` (especially `docs/ROADMAP.md`, `docs/compatibility.md`, and user guides) reflect the new release where it matters.
   - Run:
     - `python -m mkdocs build --strict`

5. **Run full checks locally**
   - From a clean environment:
     - `ruff format .`
     - `ruff check .`
     - `mypy capper`
     - `pytest capper/tests -m "not benchmark" --cov=capper --cov-report=term-missing --cov-fail-under=98`

6. **Tag the release**
   - Commit all changes.
   - Create an annotated tag: `git tag -a vX.Y.Z -m "Release X.Y.Z"`.
   - Push: `git push && git push origin vX.Y.Z`.

7. **Verify publish workflow**
   - Confirm that `.github/workflows/publish.yml` completes successfully for the new tag.
   - Check that the new version is visible on PyPI and can be installed with `pip install capper==X.Y.Z`.

8. **Update roadmap and docs index**
   - Update `docs/ROADMAP.md` milestones and “Current release” to include the new version.
   - If needed, add a short note to `docs/README.md` or other entry points highlighting major changes.

