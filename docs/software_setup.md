# Software Setup Guide

## Smart Home Energy Monitoring System

This guide explains how to set up the software components required to run the Smart Home Energy Monitoring System using the Python-based virtual smart meter architecture.

The software setup allows the complete project to run locally without physical hardware while maintaining compatibility with the ESP32 firmware architecture.

---

# Software Architecture

The software stack consists of:

```text
Python Simulator
        │
        ▼
MQTT Broker (Mosquitto)
        │
        ▼
Home Assistant
        │
        ▼
Grafana Dashboard
```

The simulator generates realistic energy-monitoring telemetry and publishes MQTT messages identical to those produced by the ESP32 firmware.

---

# Prerequisites

Install the following software before proceeding.

## Required Software

### Python

Recommended Version:

```text
Python 3.11+
```

Verify installation:

```bash
python --version
```

Expected Output:

```bash
Python 3.11.x
```

---

### Git

Verify installation:

```bash
git --version
```

Expected Output:

```bash
git version x.x.x
```

---

### Visual Studio Code

Recommended IDE:

```text
Visual Studio Code
```

Download:

https://code.visualstudio.com

Recommended Extensions:

- Python
- Pylance
- C/C++
- YAML
- Docker
- GitHub Actions

---

### Mosquitto MQTT Broker

Download:

https://mosquitto.org/download/

Verify installation:

```bash
mosquitto -v
```

Expected Output:

```text
mosquitto version x.x.x
```

---

# Clone Repository

Clone the project repository.

```bash
git clone <repository-url>
```

Enter the project directory.

```bash
cd Smart-Home-Energy-Monitoring-System
```

---

# Create Virtual Environment

Create a dedicated Python environment.

Windows:

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

# Install Dependencies

Install all required Python packages.

```bash
pip install -r requirements.txt
```

Verify installation:

```bash
pip list
```

Key packages:

```text
paho-mqtt
requests
python-dotenv
numpy
pandas
matplotlib
fpdf2
pytest
pytest-cov
PyYAML
```

---

# Environment Configuration

Copy:

```text
.env.example
```

to:

```text
.env
```

Windows:

```bash
copy .env.example .env
```

Linux/macOS:

```bash
cp .env.example .env
```

---

# Configure MQTT Settings

Open:

```text
.env
```

Example:

```env
MQTT_BROKER=localhost
MQTT_PORT=1883

MQTT_TOPIC_TELEMETRY=home/energy/node1/telemetry
MQTT_TOPIC_ALERTS=home/energy/node1/alerts
MQTT_TOPIC_STATUS=home/energy/node1/status
```

---

# Start Mosquitto Broker

Open a new terminal.

Windows:

```bash
mosquitto -v
```

or

```bash
"C:\Program Files\Mosquitto\mosquitto.exe" -v
```

Expected Output:

```text
Opening ipv4 listen socket on port 1883
```

Keep this terminal running.

---

# Run MQTT Subscriber (Optional)

Open another terminal.

Subscribe to telemetry:

```bash
mosquitto_sub -h localhost -t "home/energy/node1/telemetry" -v
```

You should see telemetry data when the simulator starts.

---

# Run the Energy Simulator

Activate the virtual environment.

```bash
venv\Scripts\activate
```

Run:

```bash
python -m simulator.main
```

Expected Output:

```text
SMART HOME ENERGY MONITORING SYSTEM

[OK] MQTT Connected
[OK] System Ready

[10:00:00] Air Conditioner | 1800 W | ...
```

The simulator will:

- Generate appliance measurements
- Calculate power consumption
- Track energy usage
- Estimate costs
- Detect alerts
- Publish MQTT telemetry
- Generate reports

---

# Generated Outputs

After execution:

## CSV Logs

Location:

```text
outputs/csv_logs/
```

Contains:

```text
timestamp
voltage
current
power
energy
cost
alerts
```

---

## PDF Reports

Location:

```text
reports/pdf/
```

Example:

```text
daily_report_YYYYMMDD.pdf
```

Contains:

- Total Energy Usage
- Estimated Cost
- Alert Summary
- Consumption Statistics

---

# Running Unit Tests

Execute:

```bash
pytest -vv
```

Expected Result:

```text
72 passed
```

---

# Home Assistant Setup

Configuration files are provided in:

```text
dashboard/home_assistant/
```

Files:

```text
mqtt.yaml
automations.yaml
```

These can be imported into a Home Assistant installation to automatically create MQTT entities and alerts.

---

# Grafana Setup

Grafana dashboard configuration is available in:

```text
dashboard/grafana/dashboard.json
```

Import the JSON file into Grafana.

Dashboard includes:

- Voltage Monitoring
- Current Monitoring
- Active Power
- Energy Consumption
- Cost Tracking
- Alert Metrics

---

# Folder Usage During Execution

Important runtime folders:

```text
outputs/csv_logs/
```

Stores generated telemetry logs.

```text
reports/pdf/
```

Stores generated PDF reports.

```text
outputs/alerts/
```

Stores alert-related exports.

```text
data/raw/
```

Stores raw collected data.

```text
data/processed/
```

Stores transformed datasets.

---

# Common Issues

## MQTT Connection Refused

Error:

```text
Connection Refused
```

Solution:

Ensure Mosquitto is running:

```bash
mosquitto -v
```

---

## Missing Python Package

Error:

```text
ModuleNotFoundError
```

Solution:

```bash
pip install -r requirements.txt
```

---

## Virtual Environment Not Activated

Error:

```text
python not recognized
```

Solution:

Activate:

```bash
venv\Scripts\activate
```

before running commands.

---

## PDF Generation Error

Ensure:

```text
fpdf2
```

is installed:

```bash
pip install fpdf2
```

---

# Verification Checklist

Confirm the following:

- Python installed
- Virtual environment created
- Requirements installed
- Mosquitto running
- MQTT subscriber receiving messages
- Simulator executing successfully
- CSV logs generated
- PDF reports generated
- Tests passing
- Home Assistant configuration available
- Grafana dashboard available

---

# Setup Complete

You now have a fully operational Smart Home Energy Monitoring System software environment capable of:

- Simulating household energy usage
- Publishing MQTT telemetry
- Tracking power consumption
- Estimating electricity costs
- Generating reports
- Integrating with Home Assistant
- Visualizing data through Grafana

without requiring physical hardware.