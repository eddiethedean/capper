"""CLI for ad-hoc fake data generation."""

import argparse
import difflib
import sys
from collections.abc import Iterator, Sequence
from typing import Mapping, Type

import capper

from .base import FakerType, faker, seed
from .registry import build_type_registry

MAX_GENERATE_COUNT = 1_000_000


def _type_registry() -> Mapping[str, Type[FakerType]]:
    """Map type name -> FakerType subclass (only types with faker_provider)."""
    return build_type_registry(capper)


def _escape_tsv(value: str) -> str:
    """Escape tabs and newlines so each logical row is a single output line."""
    return (
        value.replace("\\", "\\\\").replace("\t", "\\t").replace("\n", "\\n").replace("\r", "\\r")
    )


def _generate_one(typ: Type[FakerType]) -> str:
    """Generate a single value for the given FakerType."""
    provider = getattr(typ, "faker_provider", "")
    kwargs = dict(getattr(typ, "faker_kwargs", None) or {})
    value = getattr(faker, provider)(**kwargs)
    return _escape_tsv(str(value))


def _iter_rows(types: Sequence[Type[FakerType]], count: int) -> Iterator[str]:
    """Yield tab-separated rows for the given types without materializing all rows."""
    for _ in range(count):
        row = [_generate_one(t) for t in types]
        yield "\t".join(row)


def _unknown_type_message(name: str, registry: Mapping[str, Type[FakerType]]) -> str:
    known_names = sorted(registry)
    suggestions = difflib.get_close_matches(name, known_names, n=3)
    parts = [f"Unknown type: {name}."]
    if suggestions:
        parts.append(f" Did you mean: {', '.join(suggestions)}?")
    else:
        sample = ", ".join(known_names[:5])
        parts.append(f" Known types include: {sample}, ...")
    parts.append(" See the Capper docs or `FAKER_PROVIDERS.md` for the full list.")
    return "".join(parts)


def cmd_generate(args: argparse.Namespace) -> int:
    """Run generate subcommand."""
    if args.count < 1:
        print(
            f"Invalid --count {args.count}: must be at least 1.",
            file=sys.stderr,
        )
        return 1
    if args.count > MAX_GENERATE_COUNT:
        print(
            f"Invalid --count {args.count}: maximum is {MAX_GENERATE_COUNT}.",
            file=sys.stderr,
        )
        return 1

    registry = _type_registry()
    types: list[Type[FakerType]] = []
    for name in args.types:
        if name not in registry:
            print(_unknown_type_message(name, registry), file=sys.stderr)
            return 1
        types.append(registry[name])

    if args.seed is not None:
        seed(args.seed)

    for line in _iter_rows(types, args.count):
        print(line)
    return 0


def main() -> int:
    """Entry point for the capper CLI."""
    parser = argparse.ArgumentParser(
        prog="capper",
        description="Capper: fake data via Faker-backed types, integrated with Polyfactory.",
        epilog=(
            "Examples:\n"
            "  capper generate Name Email --count 5\n"
            "  capper generate Name Email --count 3 --seed 42\n"
            "\n"
            "Type names match the Python types, e.g. Name, Email, Address."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser(
        "generate",
        help="Generate tab-separated fake values for one or more Capper types.",
    )
    gen.add_argument(
        "types",
        nargs="+",
        metavar="TYPE",
        help="Type names (e.g. Name, Email).",
    )
    gen.add_argument("-n", "--count", type=int, default=1, help="Number of rows (default: 1).")
    gen.add_argument("-s", "--seed", type=int, default=None, help="Seed for reproducible output.")
    gen.set_defaults(func=cmd_generate)

    args = parser.parse_args()
    result: int = args.func(args)
    return result
