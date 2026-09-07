"""High-level device model for an Ovum Mira heat pump system."""

from __future__ import annotations

from modbus_connection import ModbusUnit
from modbus_connection.model import (
    ComponentGroup,
)

from .const import (
    DEFAULT_WPM_UNIT_ID,
    HSM_UNIT_ID,
)
from .data_model import OvumComponent
from .enum import (
    OvumLicense,
)
from .subsystems import Ems
from .subsystems.buffer import BufferStorage
from .subsystems.heat_pump import HeatPump
from .subsystems.heating import HeatingCircuit
from .subsystems.hot_water import HotWater
from .subsystems.hsm import Hsm
from .subsystems.probe import Probe


class OvumMira:
    """An Ovum Mira heat pump system coordinated over Modbus.

    Communicates with the HSM hydraulic unit and the heat pump (Unit 111 by
    default).
    """

    def __init__(
        self,
        license: OvumLicense | None,
        wpm_unit: ModbusUnit | int | None,
        hsm_unit: ModbusUnit | None = None,
    ) -> None:
        self._license = OvumLicense(1) if license is None else license

        if wpm_unit is None:
            wpm_unit = ModbusUnit(DEFAULT_WPM_UNIT_ID)
        elif isinstance(wpm_unit, int):
            wpm_unit = ModbusUnit(wpm_unit)

        self._wpm_unit = wpm_unit
        self._hsm_unit = hsm_unit if hsm_unit is not None else ModbusUnit(HSM_UNIT_ID)

        self.hsm = Hsm(self._hsm_unit)
        self.heating1 = HeatingCircuit(self._hsm_unit, index=1)
        self.heating2 = HeatingCircuit(self._hsm_unit, index=2)
        self.heating3 = HeatingCircuit(self._hsm_unit, index=3)
        self.heating4 = HeatingCircuit(self._hsm_unit, index=4)
        self.hot_water = HotWater(self._hsm_unit)
        self.buffer = BufferStorage(self._hsm_unit)
        self.heat_pump = HeatPump(self._wpm_unit)
        self.ems = Ems(self._hsm_unit)

        hsm_components = (
            self.hsm,
            self.heating1,
            self.heating2,
            self.heating3,
            self.heating4,
            self.hot_water,
            self.buffer,
            self.ems,
        )

        wpm_components = (self.heat_pump,)

        for component in hsm_components:
            self.restrict_fields(component)

        for component in wpm_components:
            self.restrict_fields(component)

        self._hsm_group = ComponentGroup(self._hsm_unit, hsm_components)
        self._heatpump_group = ComponentGroup(self._wpm_unit, wpm_components)

    def restrict_fields(self, component: OvumComponent) -> None:
        restricted_fields = component.restricted_fields_for_license(self._license)

        if len(restricted_fields) == 0:
            return

        component.restrict_fields(component.declared_fields.keys() - restricted_fields)

    @property
    def hsm_unit(self) -> ModbusUnit:
        """The Modbus unit for the heating manager."""
        return self._hsm_unit

    @property
    def wpm_unit(self) -> ModbusUnit:
        """The Modbus unit for the heat pump."""
        return self._wpm_unit

    @property
    def components(
        self,
    ) -> tuple[
        Hsm,
        HeatingCircuit,
        HeatingCircuit,
        HeatingCircuit,
        HeatingCircuit,
        HotWater,
        BufferStorage,
        HeatPump,
    ]:
        """All subsystems."""
        return (
            self.hsm,
            self.heating1,
            self.heating2,
            self.heating3,
            self.heating4,
            self.hot_water,
            self.buffer,
            self.heat_pump,
            self.ems,
        )

    @property
    def outdoor_temperature(self) -> float | None:
        """Current outdoor temperature from the system controller."""
        return self.hsm.outdoor_temperature

    async def async_update(self, *, notify: bool = True) -> None:
        """Refresh all subsystem components across both units."""
        await self._hsm_group.async_update(notify=notify)
        await self._heatpump_group.async_update(notify=notify)

    @classmethod
    async def async_probe(cls, hsm_unit: ModbusUnit) -> str:
        probe = Probe(hsm_unit)
        await probe.async_update()

        return probe.serial_number
