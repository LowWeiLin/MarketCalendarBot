"""Tests for market calendar bot."""

import pytest
from datetime import datetime
from main import _resolve_timezone, fetch_next_session


def test_fetch_next_session_valid_exchange():
    """Test fetching the next session for a valid exchange."""
    result = fetch_next_session("NYSE")

    assert result is not None
    assert "exchange" in result
    assert "next_open" in result
    assert "next_close" in result
    assert "timezone" in result
    assert result["exchange"] == "NYSE"
    assert isinstance(result["next_open"], datetime)
    assert isinstance(result["next_close"], datetime)
    assert result["next_close"] > result["next_open"]


def test_fetch_next_session_invalid_exchange():
    """Test fetching the next session for an invalid exchange."""
    result = fetch_next_session("INVALID_EXCHANGE")

    assert result is None


def test_resolve_timezone_gmt_plus_8():
    """Test fixed offset timezone strings like GMT+8."""
    timezone, label = _resolve_timezone("GMT+8")

    assert label == "UTC+08:00"
    assert timezone.utcoffset(datetime(2026, 3, 17, 0, 0)).total_seconds() == 28800


@pytest.mark.parametrize("exchange", ["NYSE", "LSE", "XSES"])
def test_fetch_next_session_multiple_exchanges(exchange):
    """Test fetching the next session for multiple valid exchanges."""
    result = fetch_next_session(exchange)

    assert result is not None
    assert result["exchange"] == exchange
    assert isinstance(result["next_open"], datetime)
    assert isinstance(result["next_close"], datetime)
