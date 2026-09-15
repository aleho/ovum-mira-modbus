"""Tests for the OvumMira device class."""

from __future__ import annotations

from modbus_connection.mock import MockModbusUnit

from ovum_mira_modbus import (
    OvumBufferMode,
    OvumBufferType,
    OvumEmsStatus,
    OvumHeatingCircuitMode,
    OvumHeatingCircuitOperationMode,
    OvumHeatingCircuitType,
    OvumHeatpumpStatus,
    OvumHotWaterAvailable,
    OvumHotWaterStatus,
    OvumMira,
    OvumVacationStatus,
)
from ovum_mira_modbus.addr import Addr


async def test_probe(mock_hsm_unit: MockModbusUnit) -> None:
    """Test async_probe safely reads outdoor temp and status."""
    assert await OvumMira.async_probe(mock_hsm_unit) == "mock-serial"


async def test_device_update_reads_all(device: OvumMira) -> None:
    """Test reading all values across both units via device update."""
    await device.async_update()

    # System & Outdoor
    assert device.hsm.outdoor_temperature == 12.5

    # Heating Circuit 1
    assert device.heating1.type == OvumHeatingCircuitType.RETURN
    assert device.heating1.mode == OvumHeatingCircuitMode.HEATING
    assert device.heating1.operation_mode == OvumHeatingCircuitOperationMode.COOLING
    assert device.heating1.target_pv_plus == 3
    assert device.heating1.target_pv_minus == 4
    assert device.heating1.temperature_target == 25.5
    assert device.heating1.temperature == 24.6
    assert device.heating1.room_temperature_target == 24.5
    assert device.heating1.cooling_room_temperature_target == 20.5
    assert device.heating1.room_temperature == 21.2
    assert device.heating1.vacation_status == OvumVacationStatus.YES
    assert device.heating1.vacation_status_heating_target == 16
    assert device.heating1.vacation_status_cooling_target == 30
    assert device.heating1.mode_fixed_heating_target == 20
    assert device.heating1.mode_fixed_cooling_target == 18
    assert device.heating1.heating_limit == 28.5

    # Heating Circuit 2
    assert device.heating2.room_temperature_target == 25.5
    assert device.heating2.cooling_room_temperature_target == 21.0
    assert device.heating2.room_temperature == 23.5

    # Hot Water
    assert device.hot_water.status == OvumHotWaterStatus.ON
    assert device.hot_water.available == OvumHotWaterAvailable.YES
    assert device.hot_water.temperature_target == 52
    assert device.hot_water.reservoir_temperature_target == 51.5
    assert device.hot_water.reservoir_temperature_top == 50.5
    assert device.hot_water.reservoir_temperature_bottom == 45.2

    # Buffer Storage
    assert device.buffer.type == OvumBufferType.CUBE
    assert device.buffer.mode == OvumBufferMode.COOLING
    assert device.buffer.temperature_target == 40
    assert device.buffer.temperature_top == 39.7
    assert device.buffer.temperature_bottom == 35.0

    # Heat Pump
    assert device.heat_pump.demand == 80
    assert device.heat_pump.power_consumption == 1.450
    assert device.heat_pump.power_production == 5.250
    assert device.heat_pump.status == OvumHeatpumpStatus.HEATING
    assert device.heat_pump.ontime == 89901

    # EMS
    assert device.ems.status == OvumEmsStatus.INCREASE
    assert device.ems.battery == 52
    assert device.ems.grid_power == 120
    assert device.ems.inverter_power == 8580
    assert device.ems.target_power == 5000


async def test_write_datapoints(
    device: OvumMira, mock_hsm_unit: MockModbusUnit
) -> None:
    """Test writing setpoints via datapoint methods."""
    # Write buffer storage setpoint
    await device.buffer.async_write_datapoint("temperature_target_pv", 45)
    assert mock_hsm_unit.holding[Addr.BUFFER_TEMP_TARGET_PV] == 45

    # Write heating circuit target flow temperature
    await device.heating1.async_write_datapoint("room_temperature_target", 38.5)
    # Check that registers 56053 & 56054 were updated
    assert mock_hsm_unit.holding[Addr.HEAT_CIRC_1_ROOM_TARGET] != 0
