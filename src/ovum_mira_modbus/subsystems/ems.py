from __future__ import annotations

from modbus_connection.model import enum, int32, integer

from ..addr import Addr
from ..data_model import OvumComponent
from ..enum import (
    OvumEmsStatus,
    OvumLicense,
    OvumPvReleaseStatus,
)


class Ems(OvumComponent):
    """Energy management system."""

    status = enum(Addr.EMS_STATUS, OvumEmsStatus, writable=True)
    battery = integer(Addr.EMS_BATTERY, unit="%", writable=True)
    grid_power = int32(Addr.EMS_GRID_POWER, unit="W", writable=True)
    inverter_power = int32(Addr.EMS_INVERTER_POWER, unit="W", writable=True)
    target_power = int32(Addr.EMS_TARGET_POWER, unit="W", writable=True)

    pv_release_status_hot_water = enum(Addr.PV_RELEASE_WW, OvumPvReleaseStatus)
    pv_release_status_heating = enum(Addr.PV_RELEASE_HEAT, OvumPvReleaseStatus)
    pv_release_status_stage2_hot_water = enum(
        Addr.PV_RELEASE_STAGE_2_WW,
        OvumPvReleaseStatus,
    )
    pv_release_status_stage2_heating = enum(
        Addr.PV_RELEASE_STAGE_2_HEAT,
        OvumPvReleaseStatus,
    )

    def restricted_fields_for_license(self, license: OvumLicense) -> list[str]:
        if license < 2:
            return [
                "pv_release_status_hot_water",
                "pv_release_status_heating",
                "pv_release_status_stage2_hot_water",
                "pv_release_status_stage2_heating",
            ]

        return []
