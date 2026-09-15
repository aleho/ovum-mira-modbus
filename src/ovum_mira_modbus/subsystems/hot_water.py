from __future__ import annotations

from modbus_connection.model import boolean, enum

from .. import OvumHotWaterRequestStatus
from ..addr import Addr
from ..data_model import OvumComponent, float32, integer
from ..enum import (
    OvumFreshWaterStatus,
    OvumHotWaterAvailable,
    OvumHotWaterStatus,
    OvumLicense,
    OvumVacationStatus,
)


class HotWater(OvumComponent):
    """Hot water reservoir on HSM (Warmwasser, WW)."""

    status = enum(Addr.WW_STATUS, OvumHotWaterStatus, writable=True)
    request_status = enum(Addr.WW_REQ_STATUS, OvumHotWaterRequestStatus)
    available = enum(Addr.WW_AVAILABLE, OvumHotWaterAvailable)

    temperature_target = integer(Addr.WW_TEMP_TARGET, unit="°C", writable=True)
    temperature_target_pv = integer(Addr.WW_TEMP_TARGET_PV, unit="°C", writable=True)

    reservoir_temperature_target = float32(Addr.WW_RES_TEMP_TARGET, unit="°C")
    reservoir_temperature_top = float32(Addr.WW_RES_TEMP_ACTUAL_TOP, unit="°C")
    reservoir_temperature_bottom = float32(Addr.WW_RES_TEMP_ACTUAL_BOTTOM, unit="°C")

    vacation_status = enum(Addr.WW_VACATION_STATUS, OvumVacationStatus)

    fresh_water_temperature_target = integer(
        Addr.WW_FRESH_WATER_TARGET,
        unit="°C",
        writable=True,
        min=0,
        max=65,
    )
    fresh_water_status = enum(Addr.WW_FRESH_WATER_STATUS, OvumFreshWaterStatus)

    circulation_pump_status = boolean(Addr.WW_CIRC_PUMP_STATUS)
    circulation_pump_temperature = float32(Addr.WW_CIRC_PUMP_TEMP, unit="°C")

    def restricted_fields_for_license(self, license: OvumLicense) -> tuple[str]:
        if license < 2:
            return (
                "request_status",
                "vacation_status",
                "fresh_water_temperature_target",
                "fresh_water_status",
                "circulation_pump_status",
                "circulation_pump_temperature",
            )

        return tuple()
