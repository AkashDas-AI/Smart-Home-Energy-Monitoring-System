# Testing Guide

## Smart Home Energy Monitoring System

This document describes the testing strategy, test cases, validation procedures, and expected outcomes for the Smart Home Energy Monitoring System.

The project follows a layered testing approach to ensure reliability across:

- Analytics Engine
- Alert System
- MQTT Communication
- Energy Simulator
- Reporting Components
- End-to-End System Workflow

---

# Testing Objectives

The testing process verifies that the system can:

- Generate realistic telemetry
- Calculate electrical parameters correctly
- Track energy consumption accurately
- Estimate electricity costs properly
- Detect abnormal operating conditions
- Publish MQTT messages successfully
- Generate reports without failure
- Operate continuously without crashes

---

# Testing Architecture

```text
                 Unit Tests
                      │
                      ▼

     ┌────────────────────────────────┐
     │   Analytics & Core Modules     │
     └────────────────────────────────┘
                      │
                      ▼

          Integration Testing
                      │
                      ▼

     ┌────────────────────────────────┐
     │ MQTT + Simulator + Reporting   │
     └────────────────────────────────┘
                      │
                      ▼

             System Testing
                      │
                      ▼

     ┌────────────────────────────────┐
     │ End-to-End Workflow Validation │
     └────────────────────────────────┘
```

---

# Test Environment

## Operating System

Recommended:

```text
Windows 10 / 11
```

Supported:

```text
Linux
macOS
```

---

## Python Version

```text
Python 3.11+
```

Verify:

```bash
python --version
```

---

## Testing Framework

```text
Pytest
```

Installed via:

```bash
pip install pytest
```

---

## Coverage Tool

```text
pytest-cov
```

Installed via:

```bash
pip install pytest-cov
```

---

# Test Directory Structure

```text
tests/

├── __init__.py
├── test_energy_calc.py
├── test_cost_calc.py
├── test_alert_engine.py
├── test_mqtt.py
└── test_simulator.py
```

---

# Unit Testing

## Energy Calculation Tests

File:

```text
tests/test_energy_calc.py
```

Validates:

- Energy accumulation
- kWh conversion
- Power integration
- Counter resets
- Summary generation

---

### Example

Input:

```text
Power = 1000W
Time = 1 Hour
```

Expected:

```text
1.0 kWh
```

---

## Cost Calculation Tests

File:

```text
tests/test_cost_calc.py
```

Validates:

- Flat-rate billing
- Tiered pricing
- Daily cost estimates
- Monthly cost estimates
- Cost accumulation

---

### Example

Input:

```text
10 kWh
₹8 / kWh
```

Expected:

```text
₹80
```

---

## Alert Engine Tests

File:

```text
tests/test_alert_engine.py
```

Validates:

- Overvoltage detection
- Undervoltage detection
- Overcurrent detection
- Overload detection
- Energy usage alerts
- Alert severity handling

---

### Example

Input:

```text
Voltage = 260V
```

Expected:

```text
OVERVOLTAGE
CRITICAL
```

---

## MQTT Tests

File:

```text
tests/test_mqtt.py
```

Validates:

- Payload generation
- JSON serialization
- Topic formatting
- Publisher behavior
- Connection handling

---

### Example

Expected Payload:

```json
{
  "voltage": 230.0,
  "current": 5.0
}
```

---

## Simulator Tests

File:

```text
tests/test_simulator.py
```

Validates:

- Appliance generation
- Randomized telemetry
- Data ranges
- Output structure
- Batch generation

---

### Example

Expected Output:

```json
{
  "appliance": "Air Conditioner",
  "voltage": 230.5,
  "current": 7.2
}
```

---

# Running Unit Tests

Execute:

```bash
pytest -vv
```

Expected Output:

```text
===========================
72 passed
===========================
```

---

# Running Coverage Analysis

Execute:

```bash
pytest --cov=simulator
```

Detailed Coverage:

```bash
pytest --cov=simulator --cov-report=term-missing
```

Expected:

```text
Coverage > 80%
```

---

# MQTT Testing

## Broker Validation

Start Mosquitto:

```bash
mosquitto -v
```

Expected:

```text
Opening ipv4 listen socket on port 1883
```

---

## Subscriber Validation

Open a second terminal:

```bash
mosquitto_sub -h localhost -t "home/energy/node1/telemetry" -v
```

---

## Simulator Validation

Run:

```bash
python -m simulator.main
```

Expected:

```text
[OK] MQTT Connected
```

Subscriber Output:

```json
{
  "voltage": 229.4,
  "current": 4.7,
  "active_power_w": 865.1
}
```

---

# Report Generation Testing

Run simulator:

```bash
python -m simulator.main
```

Verify files exist:

```text
outputs/csv_logs/
reports/pdf/
```

---

## CSV Validation

Expected:

```csv
timestamp,voltage,current,power,energy,cost
```

Rows should be appended automatically.

---

## PDF Validation

Expected:

```text
daily_report_YYYYMMDD.pdf
```

Verify:

- Opens successfully
- Statistics displayed
- Cost information displayed
- No formatting issues

---

# Alert System Testing

## Overvoltage Test

Input:

```text
Voltage > Maximum Threshold
```

Expected:

```text
ALERT
OVERVOLTAGE
```

---

## Overcurrent Test

Input:

```text
Current > Maximum Threshold
```

Expected:

```text
ALERT
OVERCURRENT
```

---

## High Energy Usage Test

Input:

```text
Energy > Daily Limit
```

Expected:

```text
HIGH_ENERGY_USAGE
```

---

# Simulator Validation

Run:

```bash
python -m simulator.main
```

Verify:

- Voltage values are realistic
- Current values are realistic
- Appliance names vary
- Power values remain positive
- Energy increases over time

---

### Typical Output

```text
[17:10:00]
Air Conditioner
1800 W
0.0126 kWh
₹0.01
NORMAL
```

---

# End-to-End System Testing

## Test Workflow

```text
Simulator
    │
    ▼

MQTT Broker
    │
    ▼

Home Assistant
    │
    ▼

Grafana Dashboard
```

---

### Validation Checklist

Verify:

- Simulator runs
- MQTT connects
- Messages publish
- Subscriber receives messages
- Home Assistant updates entities
- Grafana displays telemetry
- Alerts appear correctly
- Reports generate successfully

---

# Hardware Validation (ESP32 Track)

When hardware is available:

Verify:

- ESP32 boots successfully
- Wi-Fi connects
- MQTT connects
- Sensor readings update
- Telemetry publishes
- Alerts trigger correctly

---

# Performance Testing

## Long Runtime Test

Execute:

```bash
python -m simulator.main
```

Run continuously for:

```text
30 Minutes
1 Hour
4 Hours
```

Verify:

- No crashes
- Stable memory usage
- Consistent MQTT publishing

---

# Acceptance Criteria

The system is considered successful when:

- All unit tests pass
- MQTT communication works
- Simulator generates valid telemetry
- Alerts trigger correctly
- Reports generate correctly
- Home Assistant receives data
- Grafana displays data
- No runtime exceptions occur

---

# Current Test Status

Latest Validation Results:

```text
Total Tests : 72
Passed      : 72
Failed      : 0
Success     : 100%
```

---

# Test Summary

The Smart Home Energy Monitoring System has been tested across:

- Analytics Modules
- Cost Engine
- Alert Engine
- MQTT Communication
- Simulator Core
- Reporting Components

These tests ensure that both the simulator-based deployment and future ESP32 hardware deployment operate reliably within the intended system architecture.