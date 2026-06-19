# MQTT Topics Documentation

## Overview

The Smart Home Energy Monitoring System uses MQTT (Message Queuing Telemetry Transport) as the primary communication protocol between:

- Python Energy Simulator (Virtual ESP32)
- ESP32 Hardware Node
- Home Assistant
- Grafana Dashboards

Both the simulator and physical ESP32 publish data using the exact same MQTT topic structure and payload format.

This ensures that dashboards, alerts, automations, and analytics continue working regardless of whether data originates from simulated or physical hardware.

---

# MQTT Architecture

```text
Python Simulator
        │
        ▼
    MQTT Broker
        │
        ├────────► Home Assistant
        │
        └────────► Grafana

ESP32 Hardware
        │
        ▼
    MQTT Broker
```

---

# MQTT Topic Hierarchy

```text
home/
└── energy/
    └── node1/
        ├── telemetry
        ├── alerts
        └── status
```

---

# Topic 1: Telemetry

## Topic

```text
home/energy/node1/telemetry
```

## Purpose

Publishes real-time electrical measurements and energy metrics.

## Published By

- Python Simulator
- ESP32 Energy Monitor

## Consumed By

- Home Assistant
- Grafana
- MQTT Explorer
- Future Analytics Systems

## QoS

```text
0
```

## Retained Message

```text
No
```

## Publish Frequency

```text
1 second
```

## Example Payload

```json
{
  "device_id": "SIM_NODE_001",
  "timestamp": "2026-06-15T10:05:49",
  "appliance": "Air Conditioner",
  "voltage": 229.8,
  "current": 6.4,
  "apparent_power_va": 1470.7,
  "active_power_w": 1321.5,
  "reactive_power_var": 645.2,
  "power_factor": 0.90,
  "energy_kwh": 12.47,
  "estimated_cost": 106.00
}
```

---

# Topic 2: Alerts

## Topic

```text
home/energy/node1/alerts
```

## Purpose

Publishes abnormal electrical conditions detected by the alert engine.

## Published By

- Python Simulator
- ESP32 Energy Monitor

## Consumed By

- Home Assistant
- Notification Systems
- Dashboard Alert Panels

## QoS

```text
1
```

## Retained Message

```text
No
```

## Example Payload

```json
{
  "timestamp": "2026-06-15T10:06:17",
  "alert_type": "OVERCURRENT",
  "severity": "CRITICAL",
  "message": "Current exceeded safe operating threshold.",
  "current": 16.2,
  "threshold": 15.0
}
```

---

# Topic 3: Device Status

## Topic

```text
home/energy/node1/status
```

## Purpose

Publishes device connection and operational status.

## Published By

- Python Simulator
- ESP32 Energy Monitor

## Consumed By

- Home Assistant
- Monitoring Dashboards

## QoS

```text
1
```

## Retained Message

```text
Yes
```

The latest status should always remain available.

## Example Payload

```json
{
  "device_id": "SIM_NODE_001",
  "timestamp": "2026-06-15T10:05:49",
  "status": "ONLINE"
}
```

Possible values:

```text
ONLINE
OFFLINE
ERROR
RESTARTING
```

---

# Topic Naming Convention

```text
home/{system}/{node}/{message_type}
```

Example:

```text
home/energy/node1/telemetry
home/energy/node1/alerts
home/energy/node1/status
```

---

# Future Expansion

Additional nodes can be added without changing dashboards.

Examples:

```text
home/energy/node2/telemetry
home/energy/node3/telemetry
home/energy/bedroom/telemetry
home/energy/kitchen/telemetry
home/energy/living_room/telemetry
```

---

# QoS Strategy

| Topic | QoS | Reason |
|---------|---------|---------|
| telemetry | 0 | High-frequency data, occasional packet loss acceptable |
| alerts | 1 | Alerts must be delivered reliably |
| status | 1 | Device availability should be reliable |

---

# Retained Message Strategy

| Topic | Retained |
|---------|---------|
| telemetry | No |
| alerts | No |
| status | Yes |

---

# System Communication Contract

The following systems must publish identical payload structures:

### Virtual Track

```text
Python Simulator
```

### Physical Track

```text
ESP32 + Sensors
```

This guarantees:

- Same dashboards
- Same alerts
- Same automations
- Same analytics
- Same MQTT infrastructure

without modifying downstream systems.

---

# Version

```text
MQTT Contract Version: 1.0
Project: Smart Home Energy Monitoring System
Author: Akash Das
```