#!/usr/bin/env python3

"""Query an Ovum Mira heat pump system over Modbus and print every known value.

Connects over Modbus TCP and reads the device once across all known values.
"""

from __future__ import annotations

import argparse
import asyncio
import time

from modbus_connection import (
    ModbusConnection,
    ModbusTcpParams,
)
from modbus_connection.cli_helper import CountingUnit, print_component
from modbus_connection.tmodbus import TmodbusConnection

from ovum_mira_modbus import (
    DEFAULT_WPM_UNIT_ID,
    HSM_UNIT_ID,
    OvumComponent,
    OvumLicense,
    OvumMira,
)

SECTIONS: dict[str, str] = {
    "hsm": "HSM",
    "heating1": "Heating Circuit 1",
    "heating2": "Heating Circuit 2",
    "heating3": "Heating Circuit 3",
    "heating4": "Heating Circuit 4",
    "hot_water": "Hot Water",
    "buffer": "Buffer Storage",
    "heat_pump": "Heat Pump",
    "ems": "EMS",
}


async def connect(
    args: argparse.Namespace,
) -> tuple[ModbusConnection, OvumMira, CountingUnit, CountingUnit]:
    """Build the connection described by the arguments. Performs no I/O."""

    connection = TmodbusConnection(ModbusTcpParams(host=args.host, port=args.port))

    await connection.connect()

    counting_wpm = CountingUnit(connection.for_unit(args.heatpump_unit))
    counting_hsm = CountingUnit(connection.for_unit(HSM_UNIT_ID))
    licence_level = args.level

    device = OvumMira(
        license=OvumLicense(licence_level),
        wpm_unit=counting_wpm,
        hsm_unit=counting_hsm,
    )

    return (connection, device, counting_wpm, counting_hsm)


def get_component_and_attribute(
    device: OvumMira, value: str
) -> tuple[OvumComponent, str | None, str]:
    parts = value.split(".", 2)
    component = parts[0]
    attribute = parts[1] if len(parts) == 2 else None
    subsystem = getattr(device, component)

    return (
        subsystem,
        attribute,
        component,
    )


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Ovum Mira modbus query script",
        description=__doc__.splitlines()[0],
    )

    parser.add_argument("host", help="hostname or IP of the device")

    parser.add_argument(
        "-u",
        "--heatpump-unit",
        type=int,
        default=DEFAULT_WPM_UNIT_ID,
        help=(
            f"Modbus unit address for WPM (heat pump) (default: {DEFAULT_WPM_UNIT_ID})"
        ),
    )

    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=502,
        help="TCP port (default: 502)",
    )

    parser.add_argument(
        "-l",
        "--level",
        type=int,
        default=1,
        help="License  level (default: 1)",
    )

    parser.add_argument(
        "--probe",
        action="store_true",
        help="Probe connection",
    )

    parser.add_argument(
        "-a",
        "--attribute",
        help="Component (and, optionally,) attribute path to output, "
        "e.g., heating1 or heating1.mode",
    )

    return parser.parse_args(argv)


def _print(device: OvumMira) -> None:
    for attr, label in SECTIONS.items():
        print()
        print_component(getattr(device, attr), title=label)


async def _run(args: argparse.Namespace) -> int:
    (connection, device, counting_wpm, counting_hsm) = await connect(args)

    if args.attribute:
        (subsystem, attribute, component) = get_component_and_attribute(
            device, args.attribute
        )

    serial_number = None

    try:
        start = time.monotonic()

        print(f"Access code accepted: {await device.access_granted()}\n")

        if args.probe:
            serial_number = await OvumMira.async_probe(counting_hsm)
        elif args.attribute:
            await subsystem.async_update()
        else:
            await device.async_update()

        elapsed = time.monotonic() - start
    finally:
        await connection.close()

    if args.probe:
        print(f"Device reported serial number: {serial_number}")
    elif args.attribute:
        if attribute is not None:
            print(getattr(subsystem, attribute))
        else:
            print_component(subsystem, title=SECTIONS[component])
    else:
        _print(device)

    total_reads = counting_hsm.reads + counting_wpm.reads
    print(f"\nQueried in {elapsed * 1000:.0f} ms ({total_reads} Modbus reads)")

    return 0


def main() -> int:
    return asyncio.run(_run(_parse_args()))


if __name__ == "__main__":
    raise SystemExit(main())
