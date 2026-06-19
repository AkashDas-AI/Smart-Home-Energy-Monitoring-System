"""
Smart Home Energy Monitoring System - Core Simulation Package.

This package contains the foundational modules responsible for generating,
managing, and validating simulated energy-monitoring data.

The core layer serves as the heart of the virtual smart meter and provides
the primary building blocks used by analytics, reporting, and communication
modules throughout the system.

Core Responsibilities:
- Centralized configuration management
- Appliance profile definitions
- Realistic energy consumption simulation
- Alert generation and anomaly detection
- Runtime data orchestration

Modules:
- config.py
    Stores system-wide configuration values such as voltage limits,
    tariff rates, MQTT settings, and operational thresholds.

- appliance_profiles.py
    Defines realistic appliance behavior models including power
    consumption ranges and power factors.

- energy_simulator.py
    Generates synthetic electrical telemetry data that mimics
    real-world appliance energy usage.

- alert_engine.py
    Evaluates system conditions and generates warnings for
    overload, overcurrent, overvoltage, and abnormal consumption.

Design Goals:
- High cohesion
- Low coupling
- Easy extensibility
- Hardware-independent testing
- Consistent interfaces across modules

This package is intentionally isolated from MQTT publishing,
report generation, and dashboard integrations to maintain
clean separation of concerns.

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

__all__ = [
    "config",
    "appliance_profiles",
    "energy_simulator",
    "alert_engine"
]