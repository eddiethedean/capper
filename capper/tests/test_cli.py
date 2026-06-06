"""Tests for the capper CLI (generate subcommand)."""

import sys

import pytest

if sys.version_info >= (3, 10):
    from capper import cli
else:
    cli = None  # type: ignore[assignment]


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
def test_cli_seed_is_deterministic(capsys: pytest.CaptureFixture[str]) -> None:
    """Generate with --seed produces identical output on repeated runs."""
    orig_argv = sys.argv
    argv = ["capper", "generate", "Name", "Email", "--count", "3", "--seed", "42"]
    try:
        sys.argv = argv
        assert cli.main() == 0
        first = capsys.readouterr().out

        sys.argv = argv
        assert cli.main() == 0
        second = capsys.readouterr().out
    finally:
        sys.argv = orig_argv

    assert first == second
    assert first.strip()


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
def test_cli_generate_hex_color(capsys: pytest.CaptureFixture[str]) -> None:
    """CLI generate HexColor uses faker_kwargs and prints a hex color."""
    orig_argv = sys.argv
    try:
        sys.argv = ["capper", "generate", "HexColor", "--count", "1", "--seed", "7"]
        assert cli.main() == 0
        value = capsys.readouterr().out.strip()
        assert value.startswith("#") and len(value) == 7
    finally:
        sys.argv = orig_argv


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
@pytest.mark.parametrize("count", [0, -1])
def test_cli_generate_zero_or_negative_count_exits_nonzero(
    capsys: pytest.CaptureFixture[str], count: int
) -> None:
    """Zero or negative --count is rejected with a non-zero exit code."""
    orig_argv = sys.argv
    try:
        sys.argv = ["capper", "generate", "Name", "--count", str(count)]
        assert cli.main() == 1
        assert "Invalid --count" in capsys.readouterr().err
    finally:
        sys.argv = orig_argv


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
def test_cli_unknown_type_exits_nonzero_and_stderr(capsys: pytest.CaptureFixture[str]) -> None:
    """Passing an unknown type name prints to stderr and returns 1."""
    orig_argv = sys.argv
    try:
        sys.argv = ["capper", "generate", "NonExistentType", "--count", "1"]
        exit_code = cli.main()
        assert exit_code == 1
        err = capsys.readouterr().err
        assert "Unknown type" in err
        assert "NonExistentType" in err
        assert "Known types include" in err or "Did you mean" in err
    finally:
        sys.argv = orig_argv


@pytest.mark.skipif(sys.version_info < (3, 10), reason="capper CLI uses Python 3.10+ syntax")
def test_cli_typo_suggests_close_match(capsys: pytest.CaptureFixture[str]) -> None:
    """A near-miss type name triggers a 'Did you mean' suggestion."""
    orig_argv = sys.argv
    try:
        sys.argv = ["capper", "generate", "Nam", "--count", "1"]
        assert cli.main() == 1
        err = capsys.readouterr().err
        assert "Did you mean" in err
        assert "Name" in err
    finally:
        sys.argv = orig_argv
