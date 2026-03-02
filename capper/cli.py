"""CLI for ad-hoc fake data generation."""

import argparse
import sys
from typing import Mapping, Sequence, Type

import capper

from .base import FakerType, faker, seed
from .registry import build_type_registry


def _type_registry() -> Mapping[str, Type[FakerType]]:
    """Map type name -> FakerType subclass (only types with faker_provider)."""
    return build_type_registry(capper)


def _generate_one(typ: Type[FakerType]) -> str:
    """Generate a single value for the given FakerType."""
    provider = getattr(typ, "faker_provider", "")
    kwargs = getattr(typ, "faker_kwargs", None) or {}
    value = getattr(faker, provider)(**kwargs)
    return str(value)


def _generate_rows(types: Sequence[Type[FakerType]], count: int) -> list[str]:
    """Generate tab-separated rows for the given types."""
    rows: list[str] = []
    for _ in range(max(0, count)):
        row = [_generate_one(t) for t in types]
        rows.append("\t".join(row))
    return rows


def cmd_generate(args: argparse.Namespace) -> int:
    """Run generate subcommand."""
    registry = _type_registry()
    types: list[Type[FakerType]] = []
    for name in args.types:
        if name not in registry:
            known = ", ".join(sorted(registry))
            print(f"Unknown type: {name}. Known: {known}", file=sys.stderr)
            return 1
        types.append(registry[name])

    if args.seed is not None:
        seed(args.seed)

    for line in _generate_rows(types, args.count):
        print(line)
    return 0


def main() -> int:
    """Entry point for the capper CLI."""
    parser = argparse.ArgumentParser(
        prog="capper", description="Capper: fake data via Faker types."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("generate", help="Generate fake values for one or more types.")
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
