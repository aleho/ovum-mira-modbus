from __future__ import annotations

from modbus_connection.model import string

from ..addr import Addr
from ..data_model import OvumComponent, float32


class Hsm(OvumComponent):
    """HSM hydraulic indoor unit."""

    outdoor_temperature = float32(Addr.OUTDOOR_TEMP, unit="°C")
    name = string(Addr.SYS_NAME, length=10)
    serial_number = string(Addr.SERIAL_NUMBER, length=10)
    version = string(Addr.VERSION, length=4)
