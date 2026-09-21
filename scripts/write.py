#!/usr/bin/env python3

"""Writes registers of an Ovum Mira heat pump system over Modbus."""

from __future__ import annotations

import argparse
import asyncio
import time

from query import build_args_parser, connect, get_component_and_attribute


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = build_args_parser("write")

    parser.add_argument(
        "attribute",
        help="Component and attribute path, e.g., heating1.mode",
    )

    parser.add_argument(
        "value",
        help="Value",
    )

    return parser.parse_args(argv)


async def _run(args: argparse.Namespace) -> int:
    (connection, device, counting_wpm, counting_hsm) = await connect(args)

    try:
        start = time.monotonic()

        (subsystem, attribute, component) = get_component_and_attribute(
            device, args.attribute
        )

        if not attribute:
            print("No attribute specified")
            return 1

        value = args.value
        print(f'Writing value "{value}" to subsystem {component}')

        await subsystem.async_write_datapoint(attribute, value)
        await subsystem.async_update()

        print(f"New value: {getattr(subsystem, attribute)}")

        elapsed = time.monotonic() - start

    finally:
        await connection.close()

    total_reads = counting_hsm.reads + counting_wpm.reads
    print(f"\nQueried in {elapsed * 1000:.0f} ms ({total_reads} Modbus reads)")

    return 0


def main() -> int:
    return asyncio.run(_run(_parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
