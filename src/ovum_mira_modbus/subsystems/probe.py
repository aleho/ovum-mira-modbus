from __future__ import annotations

from modbus_connection.model import string

from ..addr import Addr
from ..data_model import OvumComponent


class Probe(OvumComponent):
    """Probe connection"""

    serial_number = string(Addr.SERIAL_NUMBER, length=10)
