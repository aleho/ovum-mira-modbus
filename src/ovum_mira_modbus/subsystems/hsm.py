from __future__ import annotations

from modbus_connection.model import boolean, string

from ..addr import Addr
from ..data_model import OvumComponent, float32


class Hsm(OvumComponent):
    """HSM hydraulic indoor unit."""

    outdoor_temperature = float32(Addr.OUTDOOR_TEMP, unit="°C")
    name = string(Addr.SYS_NAME, length=10)
    serial_number = string(Addr.SERIAL_NUMBER, length=10)
    version = string(Addr.VERSION, length=4)

    cascade_module_request_hot_water = boolean(Addr.WW_CASCADE_REQUEST)
    cascade_module_request_heating = boolean(Addr.HEAT_CASCADE_REQUEST)
    cascade_module_request_cooling = boolean(Addr.COOL_CASCADE_REQUEST)
