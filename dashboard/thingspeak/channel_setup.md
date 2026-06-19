# ThingSpeak Channel Setup Guide

## Smart Home Energy Monitoring System

This guide explains how to create and configure a ThingSpeak channel for the Smart Home Energy Monitoring System.

The Python simulator and future ESP32 firmware will publish energy-monitoring telemetry to ThingSpeak for real-time visualization and historical analysis.

---

# Overview

ThingSpeak is an IoT analytics platform that allows devices and applications to:

* Send sensor data
* Visualize data in charts
* Analyze trends
* Monitor system performance
* Export datasets

In this project, ThingSpeak serves as the cloud dashboard for monitoring:

* Voltage
* Current
* Active Power
* Energy Consumption
* Electricity Cost
* Power Factor
* Alert Count
* System Status

---

# Step 1: Create a ThingSpeak Account

Visit:

https://thingspeak.mathworks.com

Create a free account and log in.

---

# Step 2: Create a New Channel

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

Optional:

```text
Description:
Real-time household energy monitoring using MQTT,
ESP32, and Python simulation.
```

---

# Step 3: Configure Channel Fields

Enable all 8 fields.

## Field Mapping

| Field   | Name             |
| ------- | ---------------- |
| Field 1 | Voltage (V)      |
| Field 2 | Current (A)      |
| Field 3 | Active Power (W) |
| Field 4 | Energy (kWh)     |
| Field 5 | Cost (INR)       |
| Field 6 | Power Factor     |
| Field 7 | Alert Count      |
| Field 8 | System Status    |

Your channel should look like:

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

# Step 4: Obtain Channel Credentials

Open:

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

Do not commit API keys to GitHub.

---

# Step 5: Update .env File

Add:

```env
THINGSPEAK_CHANNEL_ID=1234567
THINGSPEAK_API_KEY=ABCDEFG123456789
```

Replace with your actual values.

---

# Step 6: Verify Configuration

Open:

```text
dashboard/thingspeak/thingspeak_config.py
```

Ensure:

```python
load_dotenv()
```

is enabled and environment variables are loaded correctly.

---

# Step 7: Test Connectivity

Run a simple connection test:

```python
from dashboard.thingspeak import ThingSpeakClient

client = ThingSpeakClient()

print(client.test_connection())
```

Expected:

```text
True
```

---

# Step 8: Connect Simulator

The simulator will publish:

```text
Voltage
Current
Power
Energy
Cost
Power Factor
Alert Count
Status
```

to ThingSpeak.

Data flow:

```text
Python Simulator
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

---

# Expected Dashboard Charts

After data starts arriving, ThingSpeak automatically generates charts for:

### Voltage Trend

```text
Field 1
```

---

### Current Trend

```text
Field 2
```

---

### Power Consumption

```text
Field 3
```

---

### Energy Consumption

```text
Field 4
```

---

### Electricity Cost

```text
Field 5
```

---

### Power Factor

```text
Field 6
```

---

### Alert Count

```text
Field 7
```

---

### System Status

```text
Field 8
```

---

# Testing Procedure

Start the simulator:

```bash
python -m simulator.main
```

Wait 1–2 minutes.

Refresh your ThingSpeak channel.

Verify that charts begin updating automatically.

---

# Screenshots for Portfolio

Save dashboard screenshots in:

```text
dashboard/thingspeak/dashboard_screenshots/
```

Recommended screenshots:

```text
dashboard_overview.png
voltage_chart.png
power_chart.png
energy_chart.png
cost_chart.png
alerts_chart.png
```

Also copy selected images to:

```text
images/dashboards/
```

for use in README documentation.

---

# Free Account Limitations

ThingSpeak free accounts typically allow:

* 8 fields per channel
* Updates approximately every 15 seconds
* Public or private channels
* Basic charting and analytics

For this project, the free tier is sufficient.

---

# Final Architecture

```text
ESP32
   │
   ├── MQTT
   │
Python Simulator
   │
   ▼
ThingSpeak Cloud
   │
   ▼
Real-Time Dashboard
```

This dashboard serves as the primary visualization layer for the Smart Home Energy Monitoring System and provides a cloud-accessible interface for monitoring energy usage from anywhere.
