# Security Policy

## Supported versions

Capper 0.5.x and the upcoming 1.0.x line are intended for production use. Supported
Python and dependency versions, as well as backport expectations, are documented in
`docs/compatibility.md`.

## Reporting a vulnerability

If you believe you have found a security vulnerability in Capper or its
configuration:

- Prefer opening a **private** report if the issue is sensitive.
- You can start by opening a GitHub issue with minimal detail and ask for a
  private follow-up, or contact the maintainer listed in `MAINTAINERS.md`.

Please include:

- A clear description of the issue and potential impact.
- Steps to reproduce, ideally with a minimal code example.
- Your environment details (Python, Capper, Faker, Polyfactory versions).

We aim to:

- Acknowledge reports in a reasonable timeframe.
- Assess impact and, if confirmed, publish a fix and a new release.
- Note security-relevant fixes in `CHANGELOG.md` where appropriate.

## Automated checks

The CI pipeline (`.github/workflows/ci.yml`) runs `pip-audit` against the installed
environment to detect known vulnerabilities in dependencies. Compatibility with the
latest Faker and Polyfactory versions is also checked periodically via the
`compat-latest` workflow.

