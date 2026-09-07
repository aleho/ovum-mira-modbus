# ovum-mira-modbus

A modern Python device library for communicating with Ovum Mira heat pump systems over Modbus TCP.

This is not an official library and not sponsored by Ovum.

---

## Overview

Ovum Mira heat pump systems expose Modbus communication across multiple Modbus units:

- **System Unit (110, "HSM")**: Heating manager registers:
    - System outdoor temperature
    - Heating Circuit 1 (HK1): target setpoint, actual flow temperature, room temperature
    - Hot Water (DHW / Warmwasser): reservoir target setpoint, top actual temperature, bottom actual temperature
    - Buffer Storage (Pufferspeicher): target setpoint, actual buffer temperature
- **Heat Pump Unit (111-118, "WPM")**: Heat pump specific registers:
    - Operating status (`HEATING`, `HOT_WATER`, `COOLING`, `DEFROSTING`, etc.)
    - Electrical power consumption (kW)
    - Thermal power production (kW)
    - Heat pump demand percentage (%)

This library models two units, the HSM and configurable WPM as typed component groups and coordinates atomic polling and
setpoint writing.

---

## Installation

```bash
pip install ovum-mira-modbus
```

To include the CLI query tool and actual Modbus backend:

```bash
pip install "ovum-mira-modbus[cli]"
```

---

## Quickstart

### Example usage

```python
from modbus_connection import (
    ModbusConnection,
    ModbusError,
    ModbusTcpParams,
)

from ovum_mira_modbus import (
    OvumMira,
    OvumLicense,
)


async def main():
    connection = PymodbusConnection(ModbusTcpParams(host="192.168.1.100", port=502))
    await connection.connect()

    # specify the license level (default: 1) according to your local device
    device = OvumMira(license=OvumLicense(2), wpm_unit=111)
    await device.async_update()

    print(f"Outdoor Temperature: {device.hsm.outdoor_temperature} °C")
    print(f"Heat Pump Status: {device.heat_pump.status.name}")
    print(f"Power Consumption: {device.heat_pump.power_consumption} kW")
    print(f"Heat Production: {device.heat_pump.power_production} kW")
    print(
        f"HK1 Flow / Target: {device.heating1.temperature} / {device.heating1.target_temperature} °C"
    )
    print(
        f"DHW Top / Target: {device.hot_water.reservoir_temperature_top} / {device.hot_water.target_temperature} °C"
    )

    # set hot water target temperature to 60 °C
    await device.hot_water.async_write_datapoint("temperature_target", 60)
    # set heating circuit photovoltaic target temperature to 25.5 °C
    await device.heating1.async_write_datapoint("room_temperature_target", 25.5)
```

---

## CLI Query Tool

A command-line script is provided to inspect an Ovum system:

```bash
# Query via Modbus TCP
bin/query.py IP_OR_HOST
```

---

## Architecture

- `OvumMira`: Top-level device class coordinating communication across both Modbus units.
- `subsystems.Hsm`: Hydraulic unit (indoor system)
- `subsystems.HeatingCircuit`: Target setpoint, actual flow temperature, and measured room temperature.
- `subsystems.HotWater`: Tank setpoint, top sensor, and bottom sensor.
- `subsystems.BufferStorage`: Buffer setpoint and actual temperature.
- `subsystems.HeatPump`: Heat pump status enum, power consumption, heat production, and demand.

---

## AI

This repository was initially generated pointing AI at the
[blog post](https://developers.home-assistant.io/blog/2026/07/05/modernizing-modbus/)
describing new features in Home Assistant's Modbus implementation. The results
were full of hallucinations and needed a lot of work.

Most structuring and implementation hints were taken from
https://github.com/Tom-Bom-badil/trovis-modbus/.

Further development, adaptations, fixes, etc. were done without any AI.

## License

Apache License 2.0. See [LICENSE](LICENSE) for details.
