from __future__ import annotations

from collections.abc import Collection

from modbus_connection.model import enum, integer

from ..addr import Addr
from ..data_model import OvumComponent, float32
from ..enum import (
    OvumHeatingCircuitMode,
    OvumHeatingCircuitOperationMode,
    OvumHeatingCircuitType,
    OvumLicense,
    OvumVacationStatus,
)


class HeatingCircuit(OvumComponent):
    """Heating Circuit 1-4 on HSM."""

    type = enum(Addr.HEAT_CIRC_1_TYPE, OvumHeatingCircuitType, stride=10)
    mode = enum(Addr.HEAT_CIRC_1_MODE, OvumHeatingCircuitMode, stride=10, writable=True)
    operation_mode = enum(
        Addr.HEAT_CIRC_1_OPERATION_MODE,
        OvumHeatingCircuitOperationMode,
        stride=25,
        writable=True,
    )

    temperature_target = float32(Addr.HEAT_CIRC_1_TARGET, stride=10, unit="°C")
    temperature = float32(Addr.HEAT_CIRC_1_ACTUAL, stride=10, unit="°C", writable=True)

    target_pv_plus = integer(
        Addr.HEAT_CIRC_1_TARGET_PLUS_PV, stride=10, unit="K", writable=True
    )
    target_pv_minus = integer(
        Addr.HEAT_CIRC_1_TARGET_MINUS_PV, stride=10, unit="K", writable=True
    )

    # this target value is supposed to be writable but reports an error
    room_temperature_target = float32(
        Addr.HEAT_CIRC_1_ROOM_TARGET, stride=10, unit="°C", writable=True
    )
    room_temperature = float32(Addr.HEAT_CIRC_1_ROOM_ACTUAL, stride=25, unit="°C")

    # this is the value that is shown on the display and can be changed
    # as opposed to the target value above that is only shown
    cooling_room_temperature_target = float32(
        Addr.HEAT_CIRC_1_COOL_ROOM_TARGET, stride=25, unit="°C", writable=True
    )

    vacation_status = enum(
        Addr.HEAT_CIRC_1_VACATION_STATUS, OvumVacationStatus, stride=25, writable=True
    )
    vacation_status_heating_target = integer(
        Addr.HEAT_CIRC_1_VACATION_HEAT_TARGET, stride=25, unit="°C", writable=True
    )
    vacation_status_cooling_target = integer(
        Addr.HEAT_CIRC_1_VACATION_COOL_TARGET, stride=25, unit="°C", writable=True
    )

    mode_fixed_heating_target = integer(
        Addr.HEAT_CIRC_1_FIXED_HEAT_TARGET, stride=25, unit="°C", writable=True
    )
    mode_fixed_cooling_target = integer(
        Addr.HEAT_CIRC_1_FIXED_COOL_TARGET, stride=25, unit="°C", writable=True
    )

    heating_limit = float32(
        Addr.HEAT_CIRC_1_HEAT_LIMIT, stride=25, unit="°C", writable=True
    )

    def restricted_fields_for_license(self, license: OvumLicense) -> Collection[str]:
        if self._index > 2:
            return self.declared_fields.keys()

        fields = []

        if license < 2:
            fields = [
                "operation_mode",
                "cooling_room_temperature_target",
                "vacation_status",
                "vacation_status_heating_target",
                "vacation_status_cooling_target",
                "mode_fixed_heating_target",
                "mode_fixed_cooling_target",
                "heating_limit",
            ]

            if self._index > 1:
                fields.append("room_temperature")

        return fields
