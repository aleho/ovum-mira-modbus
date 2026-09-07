"""Tests for CLI query script."""

from __future__ import annotations

from scripts.query import _parse_args


def test_query_args_connection() -> None:
    """Test parsing connection arguments."""
    args = _parse_args(["192.168.1.100"])
    assert args.host == "192.168.1.100"
    assert args.port == 502
    assert args.heatpump_unit == 111


def test_query_args_custom_units() -> None:
    """Test custom unit IDs."""
    args = _parse_args(["192.168.1.100", "--heatpump-unit", "112"])
    assert args.heatpump_unit == 112
