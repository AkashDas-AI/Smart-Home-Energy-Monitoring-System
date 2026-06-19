"""
Unit Tests - Cost Calculator

This test suite validates all electricity cost calculations used by
the Smart Home Energy Monitoring System.

Covered Functionality:
- Flat-rate billing
- Cost accumulation
- Cost summary generation
- Counter reset behavior
- Tiered/slab billing
- Daily cost estimation
- Monthly cost estimation

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

import pytest

from simulator.analytics.cost_calculator import (
    CostCalculator,
    TieredCostCalculator,
    calculate_cost,
    estimate_daily_cost,
    estimate_monthly_cost
)


# ==========================================================
# FUNCTION TESTS
# ==========================================================

def test_flat_rate_cost_calculation():
    """
    Verify flat-rate billing.

    Example:
    10 kWh × ₹8.50
    = ₹85.00
    """

    result = calculate_cost(
        energy_kwh=10,
        tariff_rate=8.5
    )

    assert result == 85.0


def test_daily_cost_estimation():
    """
    Verify daily estimate helper.
    """

    result = estimate_daily_cost(
        daily_energy_kwh=5
    )

    assert result > 0


def test_monthly_cost_estimation():
    """
    Verify monthly estimate helper.
    """

    result = estimate_monthly_cost(
        monthly_energy_kwh=100
    )

    assert result > 0


# ==========================================================
# COST CALCULATOR CLASS
# ==========================================================

def test_cost_calculator_initialization():
    """
    Verify calculator initializes correctly.
    """

    calculator = CostCalculator()

    assert calculator.total_cost == 0.0
    assert calculator.tariff_rate > 0


def test_cost_accumulation():
    """
    Verify cumulative cost tracking.
    """

    calculator = CostCalculator(
        tariff_rate=10
    )

    calculator.add_consumption(
        energy_kwh=5
    )

    calculator.add_consumption(
        energy_kwh=3
    )

    assert calculator.get_total_cost() == 80.0


def test_single_consumption():
    """
    Verify single interval billing.
    """

    calculator = CostCalculator(
        tariff_rate=8
    )

    result = calculator.add_consumption(
        energy_kwh=2
    )

    assert result["interval_cost"] == 16.0
    assert result["total_cost"] == 16.0


def test_reset_cost_tracking():
    """
    Verify reset functionality.
    """

    calculator = CostCalculator()

    calculator.add_consumption(
        energy_kwh=10
    )

    calculator.reset()

    assert calculator.get_total_cost() == 0.0


def test_cost_summary_generation():
    """
    Verify summary payload.
    """

    calculator = CostCalculator(
        tariff_rate=8.5
    )

    calculator.add_consumption(
        energy_kwh=10
    )

    summary = calculator.get_summary()

    assert "tariff_rate" in summary
    assert "currency" in summary
    assert "total_cost" in summary

    assert summary["tariff_rate"] == 8.5


# ==========================================================
# TIERED BILLING TESTS
# ==========================================================

def test_tiered_billing_first_slab():
    """
    50 kWh entirely in slab 1.

    50 × 6 = 300
    """

    calculator = TieredCostCalculator(
        slabs=[
            (100, 6),
            (300, 8),
            (float("inf"), 10)
        ]
    )

    result = calculator.calculate_cost(
        energy_kwh=50
    )

    assert result == 300.0


def test_tiered_billing_second_slab():
    """
    150 kWh:

    First 100 @ 6
    Next 50 @ 8

    Total = 1000
    """

    calculator = TieredCostCalculator(
        slabs=[
            (100, 6),
            (300, 8),
            (float("inf"), 10)
        ]
    )

    result = calculator.calculate_cost(
        energy_kwh=150
    )

    assert result == 1000.0


def test_tiered_billing_third_slab():
    """
    350 kWh:

    100 × 6 = 600
    200 × 8 = 1600
    50 × 10 = 500

    Total = 2700
    """

    calculator = TieredCostCalculator(
        slabs=[
            (100, 6),
            (300, 8),
            (float("inf"), 10)
        ]
    )

    result = calculator.calculate_cost(
        energy_kwh=350
    )

    assert result == 2700.0


# ==========================================================
# EDGE CASES
# ==========================================================

def test_zero_energy_cost():
    """
    Cost should be zero
    when energy consumption is zero.
    """

    result = calculate_cost(
        energy_kwh=0,
        tariff_rate=8.5
    )

    assert result == 0.0


def test_small_energy_value():
    """
    Verify tiny consumption values.
    """

    result = calculate_cost(
        energy_kwh=0.01,
        tariff_rate=8.5
    )

    assert result > 0


def test_large_energy_value():
    """
    Verify large consumption values.
    """

    result = calculate_cost(
        energy_kwh=10000,
        tariff_rate=8.5
    )

    assert result == 85000.0


# ==========================================================
# PYTEST ENTRY
# ==========================================================

if __name__ == "__main__":
    pytest.main()