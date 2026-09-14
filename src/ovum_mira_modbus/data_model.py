"""Ovum-specific component models."""

from __future__ import annotations

import math
import struct
from typing import Any

from modbus_connection.model import (
    Component,
    FloatField,
    NumberField,
)

from .enum import (
    OvumLicense,
)


def number_to_words(value: int | float) -> tuple[int, int]:
    """Convert int or float to two 16-bit big-endian words."""
    if isinstance(value, int):
        packed = struct.pack(">i", value)
    else:
        packed = struct.pack(">f", value)

    return struct.unpack(">HH", packed)


class RoundingIntegerField(NumberField):
    def __init__(
        self,
        *,
        min: float | None = None,
        max: float | None = None,
        **kwargs: Any,
    ) -> None:
        self._min = min
        self._max = max

        super().__init__(**kwargs)

    def decode(self, words: list[int], scale_exponent: int | None = None) -> Any:
        val = super().decode(words, scale_exponent)

        if (
            val is None
            or math.isnan(val)
            or (self._min is not None and self._min > val)
            or (self._max is not None and self._max < val)
        ):
            return None

        return val


class RoundingFloatField(FloatField):
    def __init__(
        self,
        *,
        precision: int = 1,
        round: int | None = None,
        min: float | None = None,
        max: float | None = None,
        **kwargs: Any,
    ) -> None:
        self._precision = precision
        self._round = round
        self._min = min
        self._max = max

        super().__init__(**kwargs)

    def decode(self, words: list[int], scale_exponent: int | None = None) -> Any:
        val = super().decode(words, scale_exponent)

        if (
            val is None
            or math.isnan(val)
            or (self._min is not None and self._min > val)
            or (self._max is not None and self._max < val)
        ):
            return None

        val = math.floor(val * 10**self._precision) / 10**self._precision

        if self._round is not None and self._round >= 0:
            val = round(val, self._round)

        return val


def integer(
    address: int,
    *,
    min: float | None = None,
    max: float | None = None,
    **kwargs: Any,
) -> FloatField:
    """Read an Ovum data point as float32.
    Per the docs, the precision is always 1, but the values returned carry more
    places, e.g., 57.0671. Rounding would not work in such cases.
    """

    return RoundingIntegerField(address=address, min=min, max=max, **kwargs)


def float32(
    address: int,
    *,
    precision: int = 1,
    round: int | None = None,
    min: float | None = None,
    max: float | None = None,
    **kwargs: Any,
) -> FloatField:
    """Read an Ovum data point as float32.
    Per the docs, the precision is always 1, but the values returned carry more
    places, e.g., 57.0671. Rounding would not work in such cases.
    """

    return RoundingFloatField(
        precision=precision,
        round=round,
        min=min,
        max=max,
        address=address,
        count=2,
        **kwargs,
    )


class OvumComponent(Component):
    """An Ovum subsystem with typed fields and write-authorization support."""

    async def async_write_datapoint(
        self,
        field: str,
        value: Any,
    ) -> None:
        """Write an Ovum data point."""
        await self.write(field, value)

    def restricted_fields_for_license(self, license: OvumLicense) -> list[str]:
        return []
