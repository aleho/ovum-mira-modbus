"""Fixtures for ovum-mira-modbus tests."""

from __future__ import annotations

import struct

import pytest
from modbus_connection.mock import MockModbusConnection, MockModbusUnit
from modbus_connection.pytest_plugin import (
    mock_modbus_connection as mock_modbus_connection,
)

from ovum_mira_modbus import (
    DEFAULT_WPM_UNIT_ID,
    HSM_UNIT_ID,
    OvumBufferMode,
    OvumBufferType,
    OvumEmsStatus,
    OvumHeatingCircuitMode,
    OvumHeatingCircuitOperationMode,
    OvumHeatingCircuitType,
    OvumHeatpumpStatus,
    OvumHotWaterAvailable,
    OvumHotWaterStatus,
    OvumLicense,
    OvumMira,
    OvumVacationStatus,
)
from ovum_mira_modbus.addr import Addr
from ovum_mira_modbus.data_model import number_to_words


def write_string(target: dict[int, int], addr: int, value: str) -> None:
    raw = characters.encode("ascii")
    raw += b"\x00"  # always terminate with null byte as per docs

    if len(raw) % 2 != 0:
        raw += b"\x00"  # padding

    for w in list(struct.unpack(f">{len(raw) // 2}H", raw)):
        target[addr] = w
        addr += 1


def write_number(target: dict[int, int], addr: int, value: int | float) -> None:
    w1, w2 = number_to_words(value)
    target[addr] = w1
    target[addr + 1] = w2


HSM_REGISTERS: dict[int, int] = {
    Addr.WW_STATUS: int(OvumHotWaterStatus.ON),
    Addr.WW_TEMP_TARGET: 52,
    Addr.WW_AVAILABLE: int(OvumHotWaterAvailable.YES),
    Addr.BUFFER_TYPE: int(OvumBufferType.CUBE),
    Addr.BUFFER_MODE: int(OvumBufferMode.COOLING),
    Addr.EMS_STATUS: int(OvumEmsStatus.INCREASE),
    Addr.EMS_BATTERY: 52,
    Addr.HEAT_CIRC_1_TYPE: OvumHeatingCircuitType.RETURN,
    Addr.HEAT_CIRC_1_MODE: OvumHeatingCircuitMode.HEATING,
    Addr.HEAT_CIRC_1_OPERATION_MODE: OvumHeatingCircuitOperationMode.COOLING,
    Addr.HEAT_CIRC_1_TARGET_PLUS_PV: 3,
    Addr.HEAT_CIRC_1_TARGET_MINUS_PV: 4,
    Addr.HEAT_CIRC_1_VACATION_STATUS: OvumVacationStatus.YES,
    Addr.HEAT_CIRC_1_VACATION_HEAT_TARGET: 16,
    Addr.HEAT_CIRC_1_VACATION_COOL_TARGET: 30,
    Addr.HEAT_CIRC_1_FIXED_HEAT_TARGET: 20,
    Addr.HEAT_CIRC_1_FIXED_COOL_TARGET: 18,
}

for reg, val in [
    (Addr.OUTDOOR_TEMP, 12.5),
    (Addr.WW_RES_TEMP_TARGET, 51.5),
    (Addr.WW_RES_TEMP_ACTUAL_TOP, 50.5),
    (Addr.WW_RES_TEMP_ACTUAL_BOTTOM, 45.2),
    (Addr.BUFFER_TEMP_TARGET, 40.0),
    (Addr.BUFFER_TEMP_ACTUAL_TOP, 39.7),
    (Addr.BUFFER_TEMP_ACTUAL_BOTTOM, 35.0),
    (Addr.HEAT_CIRC_1_TARGET, 25.5),
    (Addr.HEAT_CIRC_1_ACTUAL, 24.6),
    (Addr.HEAT_CIRC_1_ROOM_ACTUAL, 21.2),
    (Addr.HEAT_CIRC_1_ROOM_TARGET, 24.5),
    (Addr.HEAT_CIRC_1_COOL_ROOM_TARGET, 20.5),
    (Addr.HEAT_CIRC_1_HEAT_LIMIT, 28.5),
    (Addr.HEAT_CIRC_2_ROOM_ACTUAL, 23.5),
    (Addr.HEAT_CIRC_2_ROOM_TARGET, 25.5),
    (Addr.HEAT_CIRC_2_COOL_ROOM_TARGET, 21.0),
    (Addr.EMS_GRID_POWER, 120),
    (Addr.EMS_INVERTER_POWER, 8580),
    (Addr.EMS_TARGET_POWER, 5000),
]:
    write_number(HSM_REGISTERS, reg, val)

for reg, characters in [
    (Addr.SERIAL_NUMBER, "mock-serial"),
]:
    write_string(HSM_REGISTERS, reg, characters)

WPM_REGISTERS: dict[int, int] = {
    Addr.WPM_DEMAND: 80,
    Addr.WPM_STATUS: int(OvumHeatpumpStatus.HEATING),
}

for reg, val in [
    (Addr.WPM_POWER_CONSUMPTION, 1.450),
    (Addr.WPM_POWER_PRODUCTION, 5.250),
    (Addr.WPM_COMPRESSOR_ONTIME, 89901),
]:
    write_number(WPM_REGISTERS, reg, val)


@pytest.fixture
def mock_hsm_unit(mock_modbus_connection: MockModbusConnection) -> MockModbusUnit:
    """A seeded HSM unit (110)."""
    unit = mock_modbus_connection.for_unit(HSM_UNIT_ID)
    unit.holding.update(HSM_REGISTERS)
    return unit


@pytest.fixture
def mock_wpm_unit(mock_modbus_connection: MockModbusConnection) -> MockModbusUnit:
    """A seeded heat pump unit (111)."""
    unit = mock_modbus_connection.for_unit(DEFAULT_WPM_UNIT_ID)
    unit.holding.update(WPM_REGISTERS)
    return unit


@pytest.fixture
def device(mock_wpm_unit: MockModbusUnit, mock_hsm_unit: MockModbusUnit) -> OvumMira:
    """An OvumMira instance backed by seeded mock units."""
    return OvumMira(
        license=OvumLicense(3),
        wpm_unit=mock_wpm_unit,
        hsm_unit=mock_hsm_unit,
    )
