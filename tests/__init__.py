"""
Smart Home Energy Monitoring System - Test Suite Package.

This package contains all automated unit tests used to validate the
functionality, reliability, and correctness of the Smart Home Energy
Monitoring System.

The test suite verifies:

- Power calculations
- Energy calculations
- Cost estimation
- Alert generation
- Simulator output validity
- MQTT communication behavior

Testing Goals:
- Ensure analytical accuracy
- Detect regressions early
- Validate business logic
- Improve code quality
- Support CI/CD workflows

Test Modules:
- test_energy_calc.py
    Verifies energy consumption calculations.

- test_cost_calc.py
    Verifies electricity cost calculations.

- test_alert_engine.py
    Verifies alert detection logic.

- test_simulator.py
    Verifies simulator telemetry generation.

- test_mqtt.py
    Verifies MQTT publishing behavior.

Tools:
- pytest
- pytest-cov

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

__all__ = [
    "test_energy_calc",
    "test_cost_calc",
    "test_alert_engine",
    "test_simulator",
    "test_mqtt"
]