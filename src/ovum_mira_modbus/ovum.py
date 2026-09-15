"""High-level device model for an Ovum Mira heat pump system."""

from __future__ import annotations

from modbus_connection import ModbusUnit
from modbus_connection.model import (
    ComponentGroup,
    Device,
    UpdateReport,
    read_optional,
)

from .addr import Addr
from .const import (
    DEFAULT_WPM_UNIT_ID,
    HSM_UNIT_ID,
)
from .data_model import number_to_words
from .enum import OvumLicense
from .subsystems import Ems
from .subsystems.buffer import BufferStorage
from .subsystems.heat_pump import HeatPump
from .subsystems.heating import HeatingCircuit
from .subsystems.hot_water import HotWater
from .subsystems.hsm import Hsm
from .subsystems.probe import Probe


class OvumMira(Device):
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

        self.modbus_unit_wpm = wpm_unit

        super().__init__(hsm_unit if hsm_unit is not None else ModbusUnit(HSM_UNIT_ID))

        self.hsm = Hsm(self.modbus_unit)

        self.heating1 = HeatingCircuit(self.modbus_unit, index=1)
        self.heating2: HeatingCircuit | None = None
        self.heating3: HeatingCircuit | None = None
        self.heating4: HeatingCircuit | None = None

        self.hot_water = HotWater(self.modbus_unit)
        self.buffer = BufferStorage(self.modbus_unit)
        self.heat_pump = HeatPump(self.modbus_unit_wpm)
        self.ems = Ems(self.modbus_unit)

        self._heating_circuits: ComponentGroup | None = None

        self._hsm_group = ComponentGroup(
            self.modbus_unit,
            (
                self.hsm,
                self.hot_water,
                self.buffer,
                self.ems,
            ),
        )

    async def _async_setup(self) -> None:
        self.heating2 = await read_optional(HeatingCircuit(self.modbus_unit, index=2))
        self.heating3 = await read_optional(HeatingCircuit(self.modbus_unit, index=3))
        self.heating4 = await read_optional(HeatingCircuit(self.modbus_unit, index=4))

        self._heating_circuits = ComponentGroup(
            self.modbus_unit,
            (
                h
                for h in (
                    self.heating1,
                    self.heating2,
                    self.heating3,
                    self.heating4,
                )
                if h
            ),
        )

        self._restrict_fields()

    def _restrict_fields(self) -> None:
        for component in (
            self.hsm,
            self.heating1,
            self.heating2,
            self.heating3,
            self.heating4,
            self.hot_water,
            self.buffer,
            self.heat_pump,
            self.ems,
        ):
            if component is None:
                continue

            restricted_fields = component.restricted_fields_for_license(self._license)

            if len(restricted_fields) == 0:
                continue

            component.restrict_fields(
                component.declared_fields.keys() - restricted_fields
            )

    async def async_update(self) -> UpdateReport:
        """Poll all subsystem components."""
        return await self.async_poll(
            (
                "hsm",
                "heating1",
                "heating2",
                "heating3",
                "heating4",
                "hot_water",
                "buffer",
                "heat_pump",
                "ems",
            )
        )

    @classmethod
    async def async_probe(cls, hsm_unit: ModbusUnit) -> str:
        probe = Probe(hsm_unit)
        await probe.async_update()

        return probe.serial_number

    async def access_granted(self) -> bool:
        granted = await self.modbus_unit.read_holding_registers(
            Addr.ACCESS_GRANTED,
            count=1,
        )

        return True if len(granted) == 1 and granted[0] == 1 else False

    async def send_access_code(self, code: int) -> None:
        w1, w2 = number_to_words(code)

        await self.modbus_unit.write_registers(Addr.ACCESS_CODE, [w1, w2])
