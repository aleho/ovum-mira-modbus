from __future__ import annotations

from modbus_connection.model import enum, int32, integer, string

from ..addr import Addr
from ..data_model import OvumComponent, float32
from ..enum import (
    OvumHeatpumpStatus,
    OvumLicense,
)


class HeatPump(OvumComponent):
    """Heat pump power, and status on WPM."""

    name = string(Addr.SYS_NAME, length=10)
    serial_number = string(Addr.SERIAL_NUMBER, length=10)
    version = string(Addr.VERSION, length=4)
    status = enum(Addr.WPM_STATUS, OvumHeatpumpStatus)
    demand = integer(Addr.WPM_DEMAND, unit="%")
    power_consumption = float32(
        Addr.WPM_POWER_CONSUMPTION,
        unit="kW",
        precision=4,
        round=3,
    )
    power_production = float32(
        Addr.WPM_POWER_PRODUCTION,
        unit="kW",
        precision=4,
        round=3,
    )
    condenser_input = float32(Addr.WPM_CONDENSER_INPUT, unit="°C")
    condenser_output = float32(Addr.WPM_CONDENSER_OUTPUT, unit="°C")
    ontime = int32(Addr.WPM_COMPRESSOR_ONTIME, unit="min")

    def restricted_fields_for_license(self, license: OvumLicense) -> list[str]:
        if license < 2:
            return [
                # serial_number is documented as restricted but actually available
            ]

        return []
