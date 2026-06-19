# Hardware Setup Guide

## Smart Home Energy Monitoring System

This guide explains how to assemble, configure, and deploy the physical version of the Smart Home Energy Monitoring System using an ESP32 microcontroller, current sensing hardware, MQTT communication, Home Assistant, and Grafana.

The hardware implementation follows the same architecture as the Python simulator, ensuring complete compatibility between both deployment tracks.

---

# Hardware Architecture

```text
AC Load
   │
   ▼

SCT-013 Current Clamp
   │
   ▼

ESP32 Microcontroller
   │
   │ MQTT
   ▼

Mosquitto Broker
   │
   ├────────► Home Assistant
   │
   └────────► Grafana Dashboard
```

The ESP32 continuously measures electrical parameters and publishes telemetry data through MQTT.

---

# Bill of Materials (BOM)

## Core Components

| Component | Quantity |
|------------|------------|
| ESP32 Development Board | 1 |
| SCT-013 Current Clamp Sensor | 1 |
| Voltage Sensor Module (ZMPT101B) | 1 |
| Breadboard | 1 |
| Jumper Wires | As Required |
| USB Cable (ESP32) | 1 |
| Wi-Fi Network | 1 |

---

## Optional Components

| Component | Purpose |
|------------|------------|
| Relay Module | Automatic Load Control |
| Buzzer | Audible Alerts |
| Red LED | Critical Alerts |
| Yellow LED | Warning Alerts |
| Green LED | Normal Operation |
| OLED Display | Local Monitoring |
| Enclosure Box | Physical Protection |

---

# ESP32 Pin Mapping

## Default Pin Configuration

| Function | ESP32 Pin |
|------------|------------|
| Voltage Sensor | GPIO 34 |
| Current Sensor | GPIO 35 |
| Relay Module | GPIO 26 |
| Buzzer | GPIO 27 |
| Green LED | GPIO 14 |
| Yellow LED | GPIO 12 |
| Red LED | GPIO 13 |

These values should match the definitions inside:

```text
firmware/esp32/config.h
```

---

# Current Sensor Wiring

## SCT-013 Current Clamp

The SCT-013 is a non-invasive current sensor that clips around a live conductor.

### Connection

```text
SCT-013
   │
Burden Resistor
   │
Signal Conditioning Circuit
   │
ESP32 ADC Pin
```

### ESP32 Connection

| SCT-013 Output | ESP32 |
|----------------|--------|
| Signal | GPIO 35 |
| GND | GND |

---

# Voltage Sensor Wiring

## ZMPT101B Voltage Sensor

### ESP32 Connection

| ZMPT101B | ESP32 |
|------------|------------|
| VCC | 3.3V |
| GND | GND |
| OUT | GPIO 34 |

---

# LED Wiring

## Green LED

| LED Pin | ESP32 |
|----------|----------|
| Anode | GPIO 14 |
| Cathode | GND |

---

## Yellow LED

| LED Pin | ESP32 |
|----------|----------|
| Anode | GPIO 12 |
| Cathode | GND |

---

## Red LED

| LED Pin | ESP32 |
|----------|----------|
| Anode | GPIO 13 |
| Cathode | GND |

---

# Buzzer Wiring

| Buzzer Pin | ESP32 |
|------------|------------|
| Positive | GPIO 27 |
| Negative | GND |

---

# Relay Wiring

## Relay Module

| Relay Pin | ESP32 |
|------------|------------|
| VCC | 5V |
| GND | GND |
| IN | GPIO 26 |

---

# Safety Notes

## Important

Never connect mains AC voltage directly to the ESP32.

Always use:

- Isolated voltage sensing modules
- Proper burden resistors
- Signal conditioning circuits
- Approved current clamps

---

## Recommended Practice

Use:

```text
SCT-013
+
ZMPT101B
```

instead of direct mains measurement.

This significantly improves safety.

---

# Firmware Preparation

Firmware source files are located in:

```text
firmware/esp32/
```

Files:

```text
main.ino
config.h
sensors.h
sensors.cpp
energy_calc.h
energy_calc.cpp
alerts.h
alerts.cpp
mqtt_client.cpp
```

---

# Configure Wi-Fi

Open:

```cpp
config.h
```

Update:

```cpp
#define WIFI_SSID "YOUR_WIFI_NAME"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"
```

---

# Configure MQTT Broker

Update:

```cpp
#define MQTT_BROKER "192.168.1.100"
#define MQTT_PORT 1883
```

Use:

```text
localhost
```

only when testing on the same machine.

For real hardware deployment, use the IP address of the MQTT broker.

---

# Configure Device Metadata

Example:

```cpp
#define DEVICE_ID "energy_node_01"
#define DEVICE_LOCATION "Living Room"
```

---

# Install Arduino IDE

Download:

```text
https://www.arduino.cc/en/software
```

---

# Install ESP32 Board Package

Open:

```text
Arduino IDE
→ Preferences
```

Additional Board URLs:

```text
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

---

Open:

```text
Tools
→ Board
→ Boards Manager
```

Install:

```text
esp32 by Espressif Systems
```

---

# Required Arduino Libraries

Install:

## PubSubClient

Used for:

```text
MQTT Communication
```

---

## ArduinoJson

Used for:

```text
JSON Payload Generation
```

---

# Compile Firmware

Open:

```text
main.ino
```

Select:

```text
ESP32 Dev Module
```

Then:

```text
Verify
```

Expected:

```text
Compilation Successful
```

---

# Upload Firmware

Connect ESP32 via USB.

Select:

```text
Tools
→ Port
```

Choose the ESP32 COM port.

Click:

```text
Upload
```

Expected:

```text
Upload Successful
```

---

# Open Serial Monitor

Set:

```text
115200 Baud
```

Expected Output:

```text
SMART HOME ENERGY MONITORING SYSTEM

WiFi Connected
MQTT Connected
System Ready
```

---

# MQTT Verification

Subscribe using:

```bash
mosquitto_sub -h localhost -t "home/energy/node1/telemetry" -v
```

Expected:

```json
{
  "voltage": 229.5,
  "current": 4.3,
  "power_factor": 0.92,
  "active_power_w": 908.0,
  "energy_kwh": 2.41
}
```

---

# Home Assistant Integration

Files:

```text
dashboard/home_assistant/
```

Import:

```text
mqtt.yaml
automations.yaml
```

Restart Home Assistant.

Verify entities appear.

---

# Grafana Integration

Import:

```text
dashboard/grafana/dashboard.json
```

Verify:

- Voltage Panel
- Current Panel
- Power Panel
- Energy Panel
- Cost Panel
- Alert Panel

---

# Testing Checklist

Verify:

- ESP32 powers on
- Wi-Fi connects successfully
- MQTT broker reachable
- Sensor values update
- Telemetry publishes
- Home Assistant receives data
- Grafana displays metrics
- Alerts trigger correctly
- Relay operates correctly
- Buzzer and LEDs function correctly

---

# Deployment Modes

## Mode 1 — Simulator

```text
Python Simulator
      ↓
MQTT Broker
      ↓
Home Assistant
      ↓
Grafana
```

No hardware required.

---

## Mode 2 — Physical Hardware

```text
ESP32
+
SCT-013
+
ZMPT101B
      ↓
MQTT Broker
      ↓
Home Assistant
      ↓
Grafana
```

Production-ready IoT deployment.

---

# Setup Complete

The hardware environment is now ready to:

- Monitor electrical parameters
- Publish MQTT telemetry
- Detect abnormal conditions
- Trigger alerts
- Generate energy analytics
- Integrate with smart home platforms
- Visualize real-time and historical consumption data