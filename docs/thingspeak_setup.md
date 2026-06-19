# ThingSpeak Setup Guide

## Smart Home Energy Monitoring System

This guide explains how to configure, connect, and use ThingSpeak as a cloud-based visualization platform for the Smart Home Energy Monitoring System.

ThingSpeak enables real-time monitoring, historical data storage, cloud accessibility, and interactive chart generation without requiring a local dashboard installation.

The Python simulator and future ESP32 firmware can both publish telemetry data to ThingSpeak using the same architecture.

---

# Overview

ThingSpeak is an IoT analytics platform developed by MathWorks that allows devices and applications to:

* Send sensor data
* Store historical telemetry
* Visualize measurements using charts
* Analyze trends over time
* Monitor system performance remotely

In this project, ThingSpeak serves as an additional cloud dashboard alongside MQTT, Home Assistant, and Grafana.

---

# Why ThingSpeak?

ThingSpeak was selected because it provides:

* Free cloud hosting
* Easy setup
* Built-in chart generation
* Historical data storage
* Public or private channels
* MQTT and HTTP support
* MATLAB analytics integration

Benefits for this project:

* No local dashboard installation required
* Accessible from anywhere
* Suitable for portfolio demonstrations
* Simple ESP32 integration
* Supports long-term data visualization

---

# ThingSpeak Architecture

```text
ESP32 Firmware
       │
       │ HTTP API
       ▼

┌─────────────────────┐
│     ThingSpeak      │
│    Cloud Platform   │
└─────────────────────┘

       ▲
       │
       │ HTTP API
       │

Python Simulator
```

Current implementation:

```text
Python Simulator
        │
        ├── MQTT
        │
        ▼
Mosquitto Broker
        │
        ▼
Home Assistant
        │
        ▼
Grafana

        │
        │ HTTP
        ▼

ThingSpeak Cloud
```

This allows the project to support both local dashboards and cloud dashboards simultaneously.

---

# Create a ThingSpeak Account

Visit:

```text
https://thingspeak.mathworks.com
```

Create a free account and log in.

---

# Create a New Channel

Navigate to:

```text
Channels
→ My Channels
→ New Channel
```

Enter:

```text
Channel Name:
Smart Home Energy Monitoring System
```

Optional Description:

```text
IoT-based smart home energy monitoring using
Python, MQTT, ESP32, and ThingSpeak.
```

---

# Configure Channel Fields

Enable all eight available fields.

Field mapping:

| Field   | Description              |
| ------- | ------------------------ |
| Field 1 | Voltage (V)              |
| Field 2 | Current (A)              |
| Field 3 | Active Power (W)         |
| Field 4 | Energy Consumption (kWh) |
| Field 5 | Estimated Cost (INR)     |
| Field 6 | Power Factor             |
| Field 7 | Alert Count              |
| Field 8 | System Status            |

Example:

```text
Field 1 → Voltage (V)
Field 2 → Current (A)
Field 3 → Active Power (W)
Field 4 → Energy (kWh)
Field 5 → Cost (INR)
Field 6 → Power Factor
Field 7 → Alert Count
Field 8 → System Status
```

Click:

```text
Save Channel
```

---

# Obtain Channel Credentials

Navigate to:

```text
Channels
→ API Keys
```

Copy:

```text
Channel ID
Write API Key
Read API Key
```

Example:

```text
Channel ID:
1234567

Write API Key:
ABCDEFG123456789

Read API Key:
XYZ987654321
```

Important:

Never commit API keys to GitHub.

---

# Configure Environment Variables

Open:

```text
.env
```

Update:

```env
THINGSPEAK_CHANNEL_ID=1234567
THINGSPEAK_API_KEY=ABCDEFG123456789
```

Replace the example values with your actual credentials.

---

# Verify ThingSpeak Configuration

Configuration files:

```text
dashboard/thingspeak/
```

Files:

```text
thingspeak_config.py
thingspeak_client.py
```

Verify that environment variables are loaded correctly.

---

# Test Connection

Create:

```python
from dashboard.thingspeak import ThingSpeakClient

client = ThingSpeakClient()

print(
    client.test_connection()
)
```

Run:

```bash
python test_thingspeak.py
```

Expected Output:

```text
Success: True
```

This confirms that the project can communicate with the ThingSpeak API successfully.

---

# Simulator Integration

The simulator automatically publishes:

* Voltage
* Current
* Active Power
* Energy Consumption
* Electricity Cost
* Power Factor
* Alert Count
* System Status

to ThingSpeak during execution.

Data Flow:

```text
Simulator
    │
    ▼

ThingSpeak Client
    │
    ▼

ThingSpeak Cloud
    │
    ▼

Live Dashboard
```

No additional configuration is required after the connection test succeeds.

---

# Generated Charts

ThingSpeak automatically generates charts for each configured field.

### Voltage Monitoring

```text
Field 1
```

Displays:

```text
Voltage Trend
```

---

### Current Monitoring

```text
Field 2
```

Displays:

```text
Current Consumption Trend
```

---

### Active Power Monitoring

```text
Field 3
```

Displays:

```text
Real-Time Power Usage
```

---

### Energy Consumption

```text
Field 4
```

Displays:

```text
Accumulated Energy Usage
```

---

### Electricity Cost

```text
Field 5
```

Displays:

```text
Running Cost Estimation
```

---

### Power Factor

```text
Field 6
```

Displays:

```text
Power Efficiency Trend
```

---

### Alert Count

```text
Field 7
```

Displays:

```text
System Alert Activity
```

---

### System Status

```text
Field 8
```

Displays:

```text
ONLINE / OFFLINE Status
```

---

# Portfolio Screenshots

Store screenshots in:

```text
dashboard/thingspeak/dashboard_screenshots/
```

Recommended screenshots:

```text
dashboard_overview.png
voltage_chart.png
current_chart.png
power_chart.png
energy_chart.png
cost_chart.png
alerts_chart.png
```

For README usage, copy selected screenshots to:

```text
images/dashboards/
```

---

# Testing Procedure

Start the simulator:

```bash
python -m simulator.main
```

Allow the simulator to run for at least:

```text
1–2 minutes
```

Open your ThingSpeak channel and verify:

* New records appear
* Charts update automatically
* Energy values increase over time
* Cost estimates update
* Alert counts change when alerts occur

---

# Troubleshooting

## No Data Appearing

Verify:

```env
THINGSPEAK_CHANNEL_ID
THINGSPEAK_API_KEY
```

are configured correctly.

---

## Connection Test Fails

Run:

```bash
python test_thingspeak.py
```

Verify:

* Internet connection available
* API key is valid
* Channel ID is correct

---

## Charts Not Updating

Free ThingSpeak accounts typically allow updates every:

```text
15 seconds
```

Rapid updates may be ignored.

Wait a few minutes and refresh the channel page.

---

## API Key Error

Verify:

```text
Write API Key
```

is being used rather than the Read API Key.

---

# Free Account Limitations

ThingSpeak free accounts generally provide:

* 8 fields per channel
* Approximately 15-second update intervals
* Public or private channels
* Basic analytics and charting

These limits are sufficient for this project.

---

# Expected Results

After successful configuration, the system will provide:

* Real-time cloud monitoring
* Historical energy analytics
* Cost tracking
* Alert visualization
* Remote dashboard access

without requiring Home Assistant or Grafana.

---

# Final Architecture

```text
ESP32 / Python Simulator
            │
            ├── MQTT
            │
            ▼

     Mosquitto Broker
            │
            ▼

 Home Assistant + Grafana


            │
            │ HTTP API
            ▼

       ThingSpeak
            │
            ▼

 Cloud Dashboard
```

The ThingSpeak integration extends the Smart Home Energy Monitoring System with cloud-based monitoring capabilities while maintaining compatibility with the existing MQTT-based architecture.
