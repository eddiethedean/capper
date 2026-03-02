"""Tests for the capper CLI (generate subcommand)."""

import sys

import pytest

if sys.version_info >= (3, 10):
    from capper import cli
else:
    cli = None  # type: ignore[assignment]


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
def test_cli_generate_exit_zero_and_non_empty_output() -> None:
    """Invoke generate subcommand; assert exit 0 and non-empty output for a known type."""
    orig_argv = sys.argv
    try:
        sys.argv = ["capper", "generate", "Name", "--count", "1"]
        exit_code = cli.main()
        assert exit_code == 0
    finally:
        sys.argv = orig_argv


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
def test_cli_generate_produces_output(capsys: pytest.CaptureFixture[str]) -> None:
    """Generate subcommand prints one tab-separated value per row."""
    orig_argv = sys.argv
    try:
        sys.argv = ["capper", "generate", "Name", "Email", "--count", "2"]
        exit_code = cli.main()
        assert exit_code == 0
        out = capsys.readouterr().out
        lines = [line for line in out.strip().splitlines() if line.strip()]
        assert len(lines) == 2
        for line in lines:
            parts = line.split("\t")
            assert len(parts) == 2
            assert len(parts[0]) > 0 and len(parts[1]) > 0
    finally:
        sys.argv = orig_argv


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
def test_type_registry_includes_known_type() -> None:
    """Internal type registry used by CLI contains a known FakerType."""
    assert hasattr(cli, "_type_registry")
    registry = cli._type_registry()
    assert "Name" in registry
    name_type = registry["Name"]
    assert getattr(name_type, "faker_provider", "") == "name"
