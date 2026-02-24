"""Ensure docs/examples/*.py run without error (user guide code)."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Repo root: parent of capper/tests
REPO_ROOT = Path(__file__).resolve().parent.parent.parent


@pytest.mark.parametrize(
    "script",
    ["getting_started", "models_and_factories", "reproducible_data", "custom_types"],
)
def test_docs_example_runs(script: str) -> None:
    """Run each docs example script; fail if it exits non-zero."""
    path = REPO_ROOT / "docs" / "examples" / f"{script}.py"
    assert path.exists(), f"Missing {path}"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=str(REPO_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert result.returncode == 0, (
        f"docs/examples/{script}.py failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )
