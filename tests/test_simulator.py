"""
Unit Tests - Energy Simulator

This test suite validates the virtual smart meter simulation engine
used by the Smart Home Energy Monitoring System.

Covered Functionality:
- Simulator initialization
- Telemetry generation
- Batch generation
- Device metadata
- Measurement structure validation
- Data type validation
- Value range validation
- Helper function validation

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

import pytest

from simulator.core.energy_simulator import (
    EnergySimulator,
    generate_sample,
    generate_samples
)

from simulator.core.appliance_profiles import (
    appliance_count
)

from simulator.core.config import (
    DEVICE_ID,
    LOCATION,
    MIN_VOLTAGE,
    MAX_VOLTAGE
)


# ==========================================================
# INITIALIZATION TESTS
# ==========================================================

def test_simulator_initialization():
    """
    Verify simulator initializes correctly.
    """

    simulator = EnergySimulator()

    assert simulator.device_id == DEVICE_ID
    assert simulator.location == LOCATION


# ==========================================================
# TELEMETRY GENERATION TESTS
# ==========================================================

def test_generate_measurement_returns_dict():
    """
    Telemetry output should be a dictionary.
    """

    simulator = EnergySimulator()

    result = simulator.generate_measurement()

    assert isinstance(result, dict)


def test_measurement_contains_required_fields():
    """
    Verify telemetry structure.
    """

    simulator = EnergySimulator()

    result = simulator.generate_measurement()

    required_fields = [
        "device_id",
        "location",
        "timestamp",
        "appliance",
        "category",
        "is_active",
        "voltage",
        "current",
        "apparent_power_va",
        "active_power_w",
        "reactive_power_var",
        "power_factor"
    ]

    for field in required_fields:
        assert field in result


def test_measurement_data_types():
    """
    Verify telemetry data types.
    """

    simulator = EnergySimulator()

    result = simulator.generate_measurement()

    assert isinstance(
        result["device_id"],
        str
    )

    assert isinstance(
        result["location"],
        str
    )

    assert isinstance(
        result["timestamp"],
        str
    )

    assert isinstance(
        result["appliance"],
        str
    )

    assert isinstance(
        result["category"],
        str
    )

    assert isinstance(
        result["is_active"],
        bool
    )

    assert isinstance(
        result["voltage"],
        float
    )

    assert isinstance(
        result["current"],
        float
    )


# ==========================================================
# VALUE RANGE TESTS
# ==========================================================

def test_voltage_range():
    """
    Voltage should remain
    within expected limits.
    """

    simulator = EnergySimulator()

    result = simulator.generate_measurement()

    assert (
        MIN_VOLTAGE * 0.90
        <= result["voltage"]
        <= MAX_VOLTAGE * 1.10
    )


def test_current_is_positive():
    """
    Current should always
    be positive.
    """

    simulator = EnergySimulator()

    result = simulator.generate_measurement()

    assert result["current"] > 0


def test_power_values_are_positive():
    """
    Power metrics should
    be positive.
    """

    simulator = EnergySimulator()

    result = simulator.generate_measurement()

    assert (
        result["apparent_power_va"]
        >= 0
    )

    assert (
        result["active_power_w"]
        >= 0
    )

    assert (
        result["reactive_power_var"]
        >= 0
    )


def test_power_factor_range():
    """
    Power factor should
    remain between 0 and 1.
    """

    simulator = EnergySimulator()

    result = simulator.generate_measurement()

    assert (
        0.0 <=
        result["power_factor"]
        <= 1.0
    )


# ==========================================================
# BATCH GENERATION TESTS
# ==========================================================

def test_generate_batch_size():
    """
    Verify batch size.
    """

    simulator = EnergySimulator()

    batch = simulator.generate_batch(
        sample_count=10
    )

    assert len(batch) == 10


def test_batch_returns_list():
    """
    Batch output should be list.
    """

    simulator = EnergySimulator()

    batch = simulator.generate_batch(
        sample_count=5
    )

    assert isinstance(batch, list)


def test_batch_items_are_dicts():
    """
    Each batch item should
    be telemetry dictionary.
    """

    simulator = EnergySimulator()

    batch = simulator.generate_batch(
        sample_count=5
    )

    for item in batch:
        assert isinstance(
            item,
            dict
        )


# ==========================================================
# DEVICE INFO TESTS
# ==========================================================

def test_device_info():
    """
    Verify device metadata.
    """

    simulator = EnergySimulator()

    info = simulator.get_device_info()

    assert (
        info["device_id"]
        == DEVICE_ID
    )

    assert (
        info["location"]
        == LOCATION
    )

    assert (
        info["simulation_mode"]
        is True
    )

    assert (
        info["virtual_device"]
        is True
    )


# ==========================================================
# HELPER FUNCTION TESTS
# ==========================================================

def test_generate_sample_helper():
    """
    Verify helper function.
    """

    result = generate_sample()

    assert isinstance(
        result,
        dict
    )


def test_generate_samples_helper():
    """
    Verify batch helper.
    """

    result = generate_samples(
        sample_count=7
    )

    assert isinstance(
        result,
        list
    )

    assert len(result) == 7


# ==========================================================
# STABILITY TESTS
# ==========================================================

def test_multiple_measurements():
    """
    Generate multiple samples
    without failure.
    """

    simulator = EnergySimulator()

    for _ in range(100):

        result = (
            simulator
            .generate_measurement()
        )

        assert (
            isinstance(
                result,
                dict
            )
        )


def test_appliance_generation():
    """
    Verify appliance profiles
    are available.
    """

    assert appliance_count() > 0


# ==========================================================
# PYTEST ENTRY
# ==========================================================

if __name__ == "__main__":
    pytest.main()