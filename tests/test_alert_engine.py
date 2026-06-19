"""
Unit Tests - Alert Engine

This test suite validates all alert generation logic used by
the Smart Home Energy Monitoring System.

Covered Functionality:
- Overvoltage detection
- Undervoltage detection
- Overcurrent detection
- High current warnings
- Power overload detection
- High power usage warnings
- Excessive energy usage detection
- Low power factor detection
- Alert severity handling
- Alert summary generation

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

import pytest

from simulator.core.alert_engine import (
    AlertEngine,
    INFO,
    WARNING,
    CRITICAL,
    evaluate_alerts
)

from simulator.core.config import (
    MIN_VOLTAGE,
    MAX_VOLTAGE,
    WARNING_CURRENT,
    MAX_CURRENT,
    WARNING_POWER,
    MAX_POWER,
    DAILY_ENERGY_LIMIT_KWH
)


# ==========================================================
# INITIALIZATION TESTS
# ==========================================================

def test_alert_engine_initialization():
    """
    Verify engine initializes correctly.
    """

    engine = AlertEngine()

    assert engine.active_alerts == []
    assert engine.has_alerts() is False


# ==========================================================
# VOLTAGE TESTS
# ==========================================================

def test_overvoltage_detection():
    """
    Voltage above maximum threshold
    should trigger OVERVOLTAGE alert.
    """

    engine = AlertEngine()

    alerts = engine.check_voltage(
        MAX_VOLTAGE + 10
    )

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "OVERVOLTAGE"
    assert alerts[0]["severity"] == CRITICAL


def test_undervoltage_detection():
    """
    Voltage below minimum threshold
    should trigger UNDERVOLTAGE alert.
    """

    engine = AlertEngine()

    alerts = engine.check_voltage(
        MIN_VOLTAGE - 10
    )

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "UNDERVOLTAGE"
    assert alerts[0]["severity"] == CRITICAL


def test_normal_voltage():
    """
    Normal voltage should not trigger alerts.
    """

    engine = AlertEngine()

    alerts = engine.check_voltage(230)

    assert len(alerts) == 0


# ==========================================================
# CURRENT TESTS
# ==========================================================

def test_overcurrent_detection():
    """
    Current above MAX_CURRENT
    should trigger OVERCURRENT alert.
    """

    engine = AlertEngine()

    alerts = engine.check_current(
        MAX_CURRENT + 1
    )

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "OVERCURRENT"
    assert alerts[0]["severity"] == CRITICAL


def test_high_current_warning():
    """
    Current above WARNING_CURRENT
    should trigger HIGH_CURRENT warning.
    """

    engine = AlertEngine()

    alerts = engine.check_current(
        WARNING_CURRENT + 0.5
    )

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "HIGH_CURRENT"
    assert alerts[0]["severity"] == WARNING


def test_normal_current():
    """
    Safe current should not trigger alerts.
    """

    engine = AlertEngine()

    alerts = engine.check_current(5)

    assert len(alerts) == 0


# ==========================================================
# POWER TESTS
# ==========================================================

def test_power_overload_detection():
    """
    Power above MAX_POWER
    should trigger overload alert.
    """

    engine = AlertEngine()

    alerts = engine.check_power(
        MAX_POWER + 100
    )

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "POWER_OVERLOAD"
    assert alerts[0]["severity"] == CRITICAL


def test_high_power_warning():
    """
    Power above WARNING_POWER
    should trigger warning.
    """

    engine = AlertEngine()

    alerts = engine.check_power(
        WARNING_POWER + 100
    )

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "HIGH_POWER_USAGE"
    assert alerts[0]["severity"] == WARNING


def test_normal_power():
    """
    Normal power should not trigger alerts.
    """

    engine = AlertEngine()

    alerts = engine.check_power(500)

    assert len(alerts) == 0


# ==========================================================
# ENERGY TESTS
# ==========================================================

def test_high_energy_usage():
    """
    Daily energy limit exceeded.
    """

    engine = AlertEngine()

    alerts = engine.check_energy_usage(
        DAILY_ENERGY_LIMIT_KWH + 1
    )

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "HIGH_ENERGY_USAGE"


def test_normal_energy_usage():
    """
    Normal energy usage should
    not trigger alerts.
    """

    engine = AlertEngine()

    alerts = engine.check_energy_usage(2)

    assert len(alerts) == 0


# ==========================================================
# POWER FACTOR TESTS
# ==========================================================

def test_low_power_factor_detection():
    """
    Poor power factor should
    trigger warning.
    """

    engine = AlertEngine()

    alerts = engine.check_power_factor(
        0.60
    )

    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "LOW_POWER_FACTOR"
    assert alerts[0]["severity"] == WARNING


def test_normal_power_factor():
    """
    Good power factor should
    not trigger alerts.
    """

    engine = AlertEngine()

    alerts = engine.check_power_factor(
        0.95
    )

    assert len(alerts) == 0


# ==========================================================
# FULL EVALUATION TESTS
# ==========================================================

def test_full_alert_evaluation():
    """
    Multiple abnormal conditions
    should generate multiple alerts.
    """

    engine = AlertEngine()

    alerts = engine.evaluate(
        voltage=260,
        current=16,
        power_watts=3500,
        energy_kwh=20,
        power_factor=0.60
    )

    assert len(alerts) >= 4
    assert engine.has_alerts() is True


def test_no_alert_conditions():
    """
    Safe operating values should
    generate zero alerts.
    """

    engine = AlertEngine()

    alerts = engine.evaluate(
        voltage=230,
        current=4,
        power_watts=800,
        energy_kwh=2,
        power_factor=0.95
    )

    assert len(alerts) == 0


# ==========================================================
# SEVERITY TESTS
# ==========================================================

def test_highest_severity_critical():
    """
    Highest severity should be CRITICAL.
    """

    engine = AlertEngine()

    engine.evaluate(
        voltage=260,
        current=20,
        power_watts=4000,
        energy_kwh=1,
        power_factor=0.95
    )

    assert (
        engine.get_highest_severity()
        == CRITICAL
    )


def test_highest_severity_warning():
    """
    Highest severity should be WARNING.
    """

    engine = AlertEngine()

    engine.evaluate(
        voltage=230,
        current=11,
        power_watts=2100,
        energy_kwh=1,
        power_factor=0.95
    )

    assert (
        engine.get_highest_severity()
        == WARNING
    )


def test_highest_severity_info():
    """
    No alerts should return INFO.
    """

    engine = AlertEngine()

    assert (
        engine.get_highest_severity()
        == INFO
    )


# ==========================================================
# SUMMARY TESTS
# ==========================================================

def test_alert_summary():
    """
    Verify summary structure.
    """

    engine = AlertEngine()

    engine.evaluate(
        voltage=260,
        current=20,
        power_watts=3500,
        energy_kwh=20,
        power_factor=0.60
    )

    summary = (
        engine.get_alert_summary()
    )

    assert "alert_count" in summary
    assert "highest_severity" in summary
    assert "alerts" in summary

    assert summary["alert_count"] > 0


# ==========================================================
# HELPER FUNCTION TEST
# ==========================================================

def test_evaluate_alerts_helper():
    """
    Verify standalone helper function.
    """

    alerts = evaluate_alerts(
        voltage=260,
        current=20,
        power_watts=3500,
        energy_kwh=20,
        power_factor=0.60
    )

    assert isinstance(alerts, list)
    assert len(alerts) > 0


# ==========================================================
# PYTEST ENTRY
# ==========================================================

if __name__ == "__main__":
    pytest.main()