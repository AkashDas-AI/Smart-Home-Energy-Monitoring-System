# MQTT Broker Setup Guide

## Overview

This document explains how to install, configure, and verify the MQTT broker used by the Smart Home Energy Monitoring System.

The project uses:

```text
Mosquitto MQTT Broker
```

Mosquitto is one of the most widely used MQTT brokers in IoT systems and is lightweight, open-source, and beginner-friendly.

---

# System Architecture

```text
                Smart Home Energy Monitoring System

┌──────────────────────┐
│ Python Simulator     │
│ (Virtual ESP32)      │
└──────────┬───────────┘
           │
           │ MQTT
           │
           ▼
┌──────────────────────┐
│ Mosquitto Broker     │
└──────────┬───────────┘
           │
           ├──────────────► Home Assistant
           │
           └──────────────► Grafana

┌──────────────────────┐
│ ESP32 Hardware Node  │
└──────────┬───────────┘
           │
           └──────────────► Same MQTT Broker
```

---

# Why MQTT?

MQTT is ideal for IoT because it provides:

- Lightweight communication
- Low bandwidth usage
- Real-time telemetry
- Publish/Subscribe architecture
- Easy integration with ESP32
- Native Home Assistant support

---

# Installing Mosquitto (Windows)

## Step 1

Download Mosquitto:

```text
https://mosquitto.org/download/
```

Install:

```text
mosquitto-<version>-install-windows-x64.exe
```

During installation:

```text
✓ Install Service
✓ Install Broker
✓ Install Client Tools
```

---

## Step 2

Verify Installation

Open PowerShell:

```powershell
mosquitto -h
```

Expected:

```text
mosquitto version x.x.x
```

---

# Starting the Broker

Open PowerShell:

```powershell
mosquitto -v
```

Expected:

```text
mosquitto version x.x.x starting

Opening ipv4 listen socket on port 1883.
Opening ipv6 listen socket on port 1883.
```

Broker is now running.

Keep this terminal open.

---

# Default MQTT Configuration

The simulator currently uses:

```env
MQTT_BROKER=localhost
MQTT_PORT=1883
MQTT_TOPIC=home/energy/node1
```

Which means:

```text
Broker Address:
localhost

Port:
1883
```

No additional configuration is required.

---

# MQTT Topic Structure

The project uses:

```text
home/energy/node1/telemetry

home/energy/node1/alerts

home/energy/node1/status
```

See:

```text
mqtt/topics.md
```

for full details.

---

# MQTT Subscriber Test

Open a NEW terminal.

Subscribe to telemetry:

```powershell
mosquitto_sub -h localhost -t "home/energy/node1/telemetry" -v
```

Expected:

```text
home/energy/node1/telemetry
{
    "voltage":230.4,
    "current":4.2
}
```

---

# MQTT Alert Test

Subscribe to alerts:

```powershell
mosquitto_sub -h localhost -t "home/energy/node1/alerts" -v
```

Expected:

```text
home/energy/node1/alerts
{
    "alert_type":"OVERCURRENT",
    "severity":"CRITICAL"
}
```

---

# MQTT Status Test

Subscribe to status:

```powershell
mosquitto_sub -h localhost -t "home/energy/node1/status" -v
```

Expected:

```text
home/energy/node1/status
{
    "status":"ONLINE"
}
```

---

# Manual Publish Test

Publish a test message:

```powershell
mosquitto_pub `
-h localhost `
-t "home/energy/node1/status" `
-m "{\"status\":\"ONLINE\"}"
```

If subscribers receive the message, the broker is working correctly.

---

# Testing with MQTT Explorer

MQTT Explorer is a graphical MQTT monitoring tool.

Download:

```text
https://mqtt-explorer.com/
```

---

## Connection Settings

```text
Host:
localhost

Port:
1883

Protocol:
mqtt://

Username:
(blank)

Password:
(blank)
```

Connect.

You should see:

```text
home
└── energy
    └── node1
        ├── telemetry
        ├── alerts
        └── status
```

---

# Running the Simulator

Start Mosquitto:

```powershell
mosquitto -v
```

Open another terminal:

```powershell
python -m simulator.main
```

Expected:

```text
[MQTT] Connected to localhost:1883

[10:05:49]
Air Conditioner | 1321.5 W | NORMAL

[10:05:50]
Television | 112.2 W | NORMAL
```

MQTT messages should now appear in:

- MQTT Explorer
- Home Assistant
- Future Grafana dashboards

---

# Common Errors

## Connection Refused

Error:

```text
WinError 10061
```

Cause:

```text
Broker not running
```

Solution:

```powershell
mosquitto -v
```

Start the broker first.

---

## Port Already In Use

Error:

```text
Only one usage of each socket address
```

Cause:

```text
Another MQTT broker is already running.
```

Solution:

```powershell
netstat -ano | findstr 1883
```

Find and stop the conflicting process.

---

## Firewall Blocking MQTT

If connection fails:

```text
Allow Mosquitto through Windows Firewall.
```

---

# Future Hardware Integration

The ESP32 firmware will publish to the exact same topics:

```text
home/energy/node1/telemetry

home/energy/node1/alerts

home/energy/node1/status
```

This ensures:

- Same dashboards
- Same Home Assistant automations
- Same MQTT infrastructure

for both:

```text
Python Simulator
```

and

```text
ESP32 Hardware Node
```

---

# Verification Checklist

Before proceeding to Home Assistant integration:

```text
[ ] Mosquitto installed
[ ] Broker starts successfully
[ ] Simulator connects successfully
[ ] Telemetry messages received
[ ] Alert messages received
[ ] Status messages received
[ ] MQTT Explorer shows live topics
```

---

# Version

```text
MQTT Infrastructure Version: 1.0
Project: Smart Home Energy Monitoring System
Author: Akash Das
```