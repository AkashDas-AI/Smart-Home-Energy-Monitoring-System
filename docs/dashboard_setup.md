# Dashboard Setup Guide

## Smart Home Energy Monitoring System

This guide explains how to configure and use the dashboard layer of the Smart Home Energy Monitoring System.

The dashboard stack consists of:

- MQTT Broker (Mosquitto)
- Home Assistant
- Grafana

Together, these tools provide real-time monitoring, historical analytics, alert visualization, and smart-home automation capabilities.

---

# Dashboard Architecture

```text
ESP32 / Python Simulator
            │
            ▼
      MQTT Broker
       (Mosquitto)
            │
            ▼
     Home Assistant
            │
            ▼
        Grafana
            │
            ▼
     User Dashboard
```

The ESP32 hardware and Python simulator publish identical MQTT payloads, allowing the dashboard to function without modification in either deployment mode.

---

# Dashboard Objectives

The dashboard is designed to provide:

- Real-time power monitoring
- Energy consumption analytics
- Cost estimation visualization
- Alert monitoring
- Device status tracking
- Historical trend analysis

---

# Prerequisites

Before configuring the dashboard, ensure:

- Mosquitto Broker is running
- Python Simulator or ESP32 is publishing MQTT data
- MQTT topics are active
- Home Assistant is installed
- Grafana is installed

---

# MQTT Topics Used

Telemetry:

```text
home/energy/node1/telemetry
```

Alerts:

```text
home/energy/node1/alerts
```

Status:

```text
home/energy/node1/status
```

---

# Home Assistant Configuration

Configuration files are located in:

```text
dashboard/home_assistant/
```

Files:

```text
mqtt.yaml
automations.yaml
```

---

# Import MQTT Configuration

Open:

```text
Home Assistant
```

Navigate to:

```text
Settings
→ Devices & Services
```

Ensure MQTT integration is installed.

---

Copy contents from:

```text
dashboard/home_assistant/mqtt.yaml
```

into:

```text
configuration.yaml
```

or include:

```yaml
mqtt: !include mqtt.yaml
```

---

# Import Automations

Copy:

```text
dashboard/home_assistant/automations.yaml
```

into:

```text
Home Assistant automations
```

or import through:

```text
Settings
→ Automations
```

---

# Restart Home Assistant

After configuration:

```text
Settings
→ System
→ Restart
```

Expected Result:

New MQTT entities appear automatically.

---

# Home Assistant Entities

Typical entities include:

```text
sensor.home_voltage

sensor.home_current

sensor.home_active_power

sensor.home_energy_kwh

sensor.home_energy_cost

sensor.home_alert_status

sensor.home_device_status
```

---

# Verify MQTT Data

Open:

```text
Developer Tools
→ States
```

Verify values are updating.

Example:

```text
sensor.home_voltage = 228.4
sensor.home_current = 3.9
sensor.home_active_power = 816.2
```

---

# Grafana Setup

Dashboard file:

```text
dashboard/grafana/dashboard.json
```

---

# Install Grafana

Download:

```text
https://grafana.com/grafana/download
```

Default URL:

```text
http://localhost:3000
```

Default Login:

```text
admin
admin
```

---

# Configure Data Source

Depending on deployment architecture, Grafana can connect to:

- InfluxDB
- PostgreSQL
- Home Assistant
- MQTT Plugins

Recommended:

```text
Home Assistant
```

or

```text
InfluxDB
```

for long-term historical storage.

---

# Import Dashboard

Navigate to:

```text
Dashboards
→ Import
```

Upload:

```text
dashboard/grafana/dashboard.json
```

Click:

```text
Import
```

Expected Result:

Smart Home Energy Dashboard appears.

---

# Dashboard Panels

The dashboard includes several monitoring panels.

---

## Voltage Panel

Displays:

```text
Voltage (V)
```

Purpose:

Monitor supply stability.

Expected Range:

```text
220V – 240V
```

---

## Current Panel

Displays:

```text
Current (A)
```

Purpose:

Monitor appliance load demand.

---

## Active Power Panel

Displays:

```text
Power (W)
```

Purpose:

Track instantaneous electricity consumption.

---

## Apparent Power Panel

Displays:

```text
VA
```

Purpose:

Monitor total electrical demand.

---

## Reactive Power Panel

Displays:

```text
VAR
```

Purpose:

Evaluate power-factor efficiency.

---

## Energy Consumption Panel

Displays:

```text
kWh
```

Purpose:

Track cumulative energy usage.

---

## Cost Tracking Panel

Displays:

```text
Estimated Electricity Cost
```

Purpose:

Monitor financial impact of consumption.

---

## Alert Panel

Displays:

```text
Current Alert State
```

Examples:

```text
NORMAL
OVERVOLTAGE
OVERCURRENT
OVERLOAD
```

---

## Device Status Panel

Displays:

```text
ONLINE
OFFLINE
```

Purpose:

Monitor node availability.

---

# Real-Time Dashboard Flow

```text
Simulator / ESP32
          │
          ▼
   MQTT Telemetry
          │
          ▼
   Home Assistant
          │
          ▼
       Grafana
          │
          ▼
  Live Dashboard Update
```

Updates occur automatically whenever new telemetry arrives.

---

# Alert Visualization

When an alert is generated:

```text
Overvoltage
Overcurrent
Overload
```

The alert pipeline becomes:

```text
Alert Engine
      │
      ▼
MQTT Alert Topic
      │
      ▼
Home Assistant
      │
      ▼
Grafana Alert Panel
```

---

# Home Assistant Automations

Automations may be configured to:

- Send notifications
- Trigger mobile alerts
- Activate smart plugs
- Turn off devices
- Log events

Example:

```text
High Energy Usage
        │
        ▼
Send Mobile Notification
```

---

# Recommended Dashboard Layout

```text
┌────────────────────────────────────┐
│ Voltage │ Current │ Power │ Status │
├────────────────────────────────────┤
│                                    │
│      Energy Consumption Graph      │
│                                    │
├────────────────────────────────────┤
│ Cost Analysis │ Alert Summary      │
├────────────────────────────────────┤
│ Historical Trends & Analytics      │
└────────────────────────────────────┘
```

---

# Testing Procedure

Start MQTT Broker:

```bash
mosquitto -v
```

Run Simulator:

```bash
python -m simulator.main
```

Verify:

- MQTT messages received
- Home Assistant entities update
- Grafana panels update
- Alerts appear correctly

---

# Troubleshooting

## Dashboard Not Updating

Check:

```bash
mosquitto_sub -h localhost -t "home/energy/node1/telemetry" -v
```

If no data appears:

- Verify simulator is running
- Verify MQTT broker is running

---

## Home Assistant Entities Missing

Verify:

```yaml
mqtt:
```

configuration is loaded.

Restart Home Assistant.

---

## Grafana Panels Empty

Verify:

- Data source configured correctly
- MQTT/Home Assistant integration active
- Incoming telemetry exists

---

# Expected Final Result

A fully operational monitoring dashboard capable of displaying:

- Voltage
- Current
- Power
- Power Factor
- Energy Consumption
- Cost Estimation
- Device Status
- System Alerts

in real time using the same MQTT architecture shared by both the ESP32 hardware implementation and the Python simulator.