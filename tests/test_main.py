"""Tests for main.py."""

import pytest
from main import parse_hours


class TestParseHours:
    """Tests for parse_hours function."""

    def test_valid_hours(self):
        assert parse_hours("24") == 24
        assert parse_hours("1") == 1
        assert parse_hours("8760") == 8760

    def test_invalid_non_integer(self):
        with pytest.raises(ValueError, match="must be an integer"):
            parse_hours("abc")

    def test_invalid_float(self):
        with pytest.raises(ValueError, match="must be an integer"):
            parse_hours("24.5")

    def test_invalid_zero(self):
        with pytest.raises(ValueError, match="must be at least 1"):
            parse_hours("0")

    def test_invalid_negative(self):
        with pytest.raises(ValueError, match="must be at least 1"):
            parse_hours("-1")

    def test_invalid_too_large(self):
        with pytest.raises(ValueError, match="cannot exceed 8760"):
            parse_hours("9000")


class TestMain:
    """Tests for main entry point."""

    def test_missing_hours_parameter(self):
        class MockRequest:
            args = {}

        from main import main
        result, status = main(MockRequest())
        assert status == 400
        assert "Missing" in result["error"]

    def test_invalid_hours_parameter(self):
        class MockRequest:
            args = {"hours": "invalid"}

        from main import main
        result, status = main(MockRequest())
        assert status == 400
        assert "integer" in result["error"]
