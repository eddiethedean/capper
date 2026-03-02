"""CLI for ad-hoc fake data generation."""

import argparse
import difflib
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
    registry = _type_registry()
    types: list[Type[FakerType]] = []
    for name in args.types:
        if name not in registry:
            print(_unknown_type_message(name, registry), file=sys.stderr)
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
