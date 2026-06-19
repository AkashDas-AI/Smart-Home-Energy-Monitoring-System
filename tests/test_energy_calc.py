"""
Unit Tests - Energy Calculator

This test suite validates all energy consumption calculations used by
the Smart Home Energy Monitoring System.

Covered Functionality:
- Wh calculation
- kWh calculation
- Running energy accumulation
- Summary generation
- Counter reset behavior

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

import pytest

from simulator.analytics.energy_calculator import (
    EnergyCalculator,
    calculate_energy_wh,
    calculate_energy_kwh
)


# ==========================================================
# FUNCTION TESTS
# ==========================================================

def test_calculate_energy_wh():
    """
    Test Wh calculation.

    1000 W running for 1 hour
    should consume 1000 Wh.
    """

    result = calculate_energy_wh(
        power_watts=1000,
        duration_seconds=3600
    )

    assert result == 1000.0


def test_calculate_energy_kwh():
    """
    Test kWh calculation.

    1000 W running for 1 hour
    should consume 1.0 kWh.
    """

    result = calculate_energy_kwh(
        power_watts=1000,
        duration_seconds=3600
    )

    assert result == 1.0


# ==========================================================
# CLASS TESTS
# ==========================================================

def test_energy_calculator_initialization():
    """
    Verify calculator starts with
    zero accumulated energy.
    """

    calculator = EnergyCalculator()

    assert calculator.total_energy_wh == 0.0
    assert calculator.total_energy_kwh == 0.0


def test_add_consumption():
    """
    Verify accumulated energy tracking.
    """

    calculator = EnergyCalculator()

    result = calculator.add_consumption(
        power_watts=1000,
        duration_seconds=3600
    )

    assert result["interval_energy_wh"] == 1000.0
    assert result["interval_energy_kwh"] == 1.0
    assert result["total_energy_wh"] == 1000.0
    assert result["total_energy_kwh"] == 1.0


def test_multiple_energy_accumulations():
    """
    Verify multiple consumption events
    accumulate correctly.
    """

    calculator = EnergyCalculator()

    calculator.add_consumption(
        power_watts=1000,
        duration_seconds=3600
    )

    calculator.add_consumption(
        power_watts=500,
        duration_seconds=3600
    )

    assert calculator.get_total_energy_wh() == 1500.0
    assert calculator.get_total_energy_kwh() == 1.5


def test_reset_energy_counters():
    """
    Verify reset functionality.
    """

    calculator = EnergyCalculator()

    calculator.add_consumption(
        power_watts=1000,
        duration_seconds=3600
    )

    calculator.reset()

    assert calculator.get_total_energy_wh() == 0.0
    assert calculator.get_total_energy_kwh() == 0.0


def test_summary_generation():
    """
    Verify summary payload.
    """

    calculator = EnergyCalculator()

    calculator.add_consumption(
        power_watts=2000,
        duration_seconds=3600
    )

    summary = calculator.get_summary()

    assert "total_energy_wh" in summary
    assert "total_energy_kwh" in summary

    assert summary["total_energy_wh"] == 2000.0
    assert summary["total_energy_kwh"] == 2.0


# ==========================================================
# EDGE CASES
# ==========================================================

def test_zero_power_consumption():
    """
    Energy should remain zero
    when power is zero.
    """

    result = calculate_energy_wh(
        power_watts=0,
        duration_seconds=3600
    )

    assert result == 0.0


def test_zero_duration():
    """
    Energy should remain zero
    when duration is zero.
    """

    result = calculate_energy_wh(
        power_watts=1000,
        duration_seconds=0
    )

    assert result == 0.0


def test_small_energy_values():
    """
    Verify handling of tiny intervals.
    """

    calculator = EnergyCalculator()

    result = calculator.add_consumption(
        power_watts=100,
        duration_seconds=1
    )

    assert result["interval_energy_wh"] > 0
    assert result["interval_energy_kwh"] > 0


# ==========================================================
# PYTEST ENTRY
# ==========================================================

if __name__ == "__main__":
    pytest.main()