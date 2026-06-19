# MQTT Architecture

## Smart Home Energy Monitoring System

This document explains the MQTT communication architecture used in the Smart Home Energy Monitoring System.

MQTT serves as the central communication layer between:

- ESP32 Energy Monitoring Node
- Python Energy Simulator
- Mosquitto MQTT Broker
- Home Assistant
- Grafana Dashboards

The architecture is intentionally designed so that both the physical and virtual implementations publish identical MQTT payloads, ensuring complete interoperability.

---

# Why MQTT?

MQTT (Message Queuing Telemetry Transport) is a lightweight publish-subscribe messaging protocol designed for Internet of Things (IoT) systems.

Advantages:

- Lightweight communication
- Low bandwidth usage
- Real-time messaging
- Event-driven architecture
- Hardware-friendly
- Easy integration with cloud and edge platforms

MQTT is widely used in:

- Smart Homes
- Industrial IoT
- Building Automation
- Energy Monitoring Systems
- Smart Cities

---

# High-Level Architecture

```text
                    ┌─────────────────────┐
                    │     ESP32 Node      │
                    └──────────┬──────────┘
                               │
                               │ MQTT Publish
                               │
                               ▼

                    ┌─────────────────────┐
                    │  Mosquitto Broker   │
                    └──────────┬──────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼

┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│ Python         │   │ Home Assistant │   │ MQTT Clients   │
│ Simulator      │   │ Subscriber     │   │ Monitoring     │
└────────────────┘   └────────────────┘   └────────────────┘
                               │
                               ▼

                    ┌─────────────────────┐
                    │      Grafana        │
                    │ Visualization Layer │
                    └─────────────────────┘
```

---

# Communication Model

MQTT uses a publish-subscribe model.

The publisher sends data to a topic.

The subscriber listens to that topic.

The publisher and subscriber never communicate directly.

Instead:

```text
Publisher
    │
    ▼
MQTT Broker
    │
    ▼
Subscriber
```

This architecture improves scalability and decouples system components.

---

# System Publishers

## ESP32 Firmware

Publishes:

```text
Voltage
Current
Power
Energy
Alerts
Status
```

Topic Examples:

```text
home/energy/node1/telemetry
home/energy/node1/alerts
home/energy/node1/status
```

---

## Python Simulator

Publishes the exact same payload structure as the ESP32 firmware.

Benefits:

- No hardware dependency
- Local development support
- Easy recruiter demonstration
- Identical dashboard behavior

---

# System Subscribers

## Home Assistant

Subscribes to:

```text
home/energy/node1/telemetry
home/energy/node1/alerts
home/energy/node1/status
```

Purpose:

- Entity creation
- Automation rules
- Alert notifications
- Smart home integration

---

## MQTT Monitoring Tools

Examples:

```text
mosquitto_sub
MQTT Explorer
MQTTX
```

Used for:

- Debugging
- Development
- Validation

---

# MQTT Broker

## Mosquitto

The project uses:

```text
Eclipse Mosquitto
```

as the MQTT broker.

Responsibilities:

- Receive published messages
- Route messages to subscribers
- Maintain client connections
- Manage retained messages

Default Configuration:

```text
Host: localhost
Port: 1883
Protocol: MQTT
```

---

# MQTT Topic Structure

The project follows a hierarchical topic naming convention.

```text
home
 └── energy
      └── node1
           ├── telemetry
           ├── alerts
           └── status
```

---

# Topic Definitions

## Telemetry Topic

Topic:

```text
home/energy/node1/telemetry
```

Purpose:

Real-time electrical measurements.

Contains:

- Voltage
- Current
- Power Factor
- Active Power
- Reactive Power
- Apparent Power
- Energy Consumption
- Cost Estimates

---

## Alerts Topic

Topic:

```text
home/energy/node1/alerts
```

Purpose:

Safety and anomaly notifications.

Examples:

- Overvoltage
- Undervoltage
- Overcurrent
- Overload
- High Energy Usage

---

## Status Topic

Topic:

```text
home/energy/node1/status
```

Purpose:

Node health monitoring.

Examples:

```text
ONLINE
OFFLINE
RECONNECTING
```

---

# Telemetry Payload Example

```json
{
  "device_id": "node1",
  "voltage": 229.5,
  "current": 4.1,
  "power_factor": 0.92,
  "apparent_power_va": 940.95,
  "active_power_w": 865.67,
  "reactive_power_var": 367.43,
  "energy_kwh": 12.51,
  "estimated_cost": 100.08,
  "timestamp": "2026-06-15T10:00:00"
}
```

---

# Alert Payload Example

```json
{
  "device_id": "node1",
  "alert_type": "OVERCURRENT",
  "severity": "WARNING",
  "message": "Current exceeded threshold",
  "timestamp": "2026-06-15T10:05:00"
}
```

---

# Status Payload Example

```json
{
  "device_id": "node1",
  "status": "ONLINE",
  "timestamp": "2026-06-15T10:00:00"
}
```

---

# MQTT Message Flow

## Normal Operation

```text
ESP32 / Simulator
        │
        ▼
Publish Telemetry
        │
        ▼
Mosquitto Broker
        │
        ▼
Home Assistant
        │
        ▼
Grafana Dashboard
```

---

## Alert Flow

```text
High Current Detected
        │
        ▼
Alert Engine
        │
        ▼
Publish Alert Topic
        │
        ▼
Mosquitto Broker
        │
        ▼
Home Assistant
        │
        ▼
Notification Triggered
```

---

# Quality of Service (QoS)

MQTT supports three delivery levels.

## QoS 0

```text
At Most Once
```

No delivery guarantee.

Fastest option.

---

## QoS 1

```text
At Least Once
```

Message guaranteed.

Possible duplicates.

Recommended for telemetry.

---

## QoS 2

```text
Exactly Once
```

Highest reliability.

Highest overhead.

Usually unnecessary for home monitoring systems.

---

# Retained Messages

Used for:

```text
Node Status
```

Example:

```json
{
  "status": "ONLINE"
}
```

New subscribers immediately receive the latest retained state.

---

# MQTT Security Considerations

For production deployments:

Use:

- Username Authentication
- Password Authentication
- TLS Encryption
- Firewall Rules

Avoid exposing MQTT brokers directly to the public internet.

---

# Scaling the Architecture

Current:

```text
home/energy/node1
```

Future:

```text
home/energy/node1
home/energy/node2
home/energy/node3
home/energy/node4
```

Multi-room deployment:

```text
home/energy/living_room
home/energy/kitchen
home/energy/bedroom
home/energy/garage
```

---

# Development Testing

Subscribe to telemetry:

```bash
mosquitto_sub -h localhost -t "home/energy/node1/telemetry" -v
```

Subscribe to alerts:

```bash
mosquitto_sub -h localhost -t "home/energy/node1/alerts" -v
```

Subscribe to status:

```bash
mosquitto_sub -h localhost -t "home/energy/node1/status" -v
```

---

# Architecture Benefits

This MQTT architecture provides:

- Real-time communication
- Hardware/software interoperability
- Scalable device management
- Home Assistant compatibility
- Grafana integration
- Easy debugging
- Industry-standard IoT design

The same architecture supports both the Python simulator and the ESP32 hardware implementation, making the project suitable for development, testing, demonstrations, and real-world deployment.