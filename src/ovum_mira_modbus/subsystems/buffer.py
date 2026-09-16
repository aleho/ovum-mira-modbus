from __future__ import annotations

from modbus_connection.model import enum, integer

from ..addr import Addr
from ..data_model import OvumComponent, float32
from ..enum import (
    OvumBufferLoadingStatus,
    OvumBufferMode,
    OvumBufferType,
    OvumCoolBufferAvailable,
    OvumCoolBufferLoadingStatus,
    OvumLicense,
)


class BufferStorage(OvumComponent):
    """Buffer for heating and cooling on HSM."""

    # A definition is needed here because reading more than one register above
    # BUFFER_LOADING_STATUS results in exception 0x02.
    register_ranges = (
        (Addr.BUFFER_TYPE, Addr.BUFFER_LOADING_STATUS),
        (Addr.COOL_BUFFER_AVAILABLE, Addr.COOL_BUFFER_LOADING_STATUS),
    )

    type = enum(Addr.BUFFER_TYPE, OvumBufferType)
    mode = enum(Addr.BUFFER_MODE, OvumBufferMode)
    loading_status = enum(Addr.BUFFER_LOADING_STATUS, OvumBufferLoadingStatus)

    temperature_target = float32(Addr.BUFFER_TEMP_TARGET, unit="°C")
    temperature_target_pv = integer(
        Addr.BUFFER_TEMP_TARGET_PV, unit="°C", writable=True
    )

    # validating min=0; with a temp sensor missing, invalid values will be returned
    temperature_top = float32(Addr.BUFFER_TEMP_ACTUAL_TOP, unit="°C", min=0)
    temperature_bottom = float32(Addr.BUFFER_TEMP_ACTUAL_BOTTOM, unit="°C", min=0)

    cooling_available = enum(Addr.COOL_BUFFER_AVAILABLE, OvumCoolBufferAvailable)
    cooling_temperature_bottom = float32(
        Addr.COOL_BUFFER_TEMP_ACTUAL_BOTTOM,
        unit="°C",
        min=0,
    )
    cooling_temperature_target = float32(Addr.COOL_BUFFER_TEMP_TARGET, unit="°C")
    cooling_loading_status = enum(
        Addr.COOL_BUFFER_LOADING_STATUS,
        OvumCoolBufferLoadingStatus,
    )

    def restricted_fields_for_license(self, license: OvumLicense) -> tuple[str]:
        if license < 2:
            return (
                "mode",
                "loading_status",
                "cooling_available",
                "cooling_status",
                "cooling_temperature_bottom",
                "cooling_temperature_target",
                "cooling_loading_status",
            )

        return tuple()
