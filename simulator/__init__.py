"""
Smart Home Energy Monitoring System - Simulator Package.

This package contains all Python-based simulation modules used to emulate a
real-world IoT Smart Home Energy Monitoring System without requiring physical
hardware.

The simulator acts as a virtual smart energy meter by generating realistic
electrical telemetry such as voltage, current, active power, apparent power,
energy consumption, and estimated electricity costs. The generated data can be
processed locally, exported to reports, and transmitted to MQTT brokers exactly
as an ESP32-based deployment would operate in production.

The architecture is intentionally designed to mirror industrial IoT energy
monitoring platforms used in smart homes, commercial buildings, manufacturing
facilities, and energy management systems.

Key Capabilities:

* Realistic appliance-level energy consumption simulation
* Voltage and current generation with configurable variability
* Active, apparent, and reactive power calculations
* Energy consumption tracking (Wh / kWh)
* Electricity cost estimation using configurable tariffs
* MQTT publishing for dashboard integration
* Real-time alert generation for abnormal conditions
* CSV and PDF report generation
* Hardware-independent testing and development

System Highlights:

* Modular and scalable package architecture
* Separation of simulation, analytics, reporting, and communication layers
* Consistent data model between simulator and ESP32 firmware
* Designed for Home Assistant, Grafana, and MQTT ecosystems
* Config-driven thresholds and operational parameters
* Beginner-friendly while following industry-oriented design practices

Difficulty Level:
Beginner → Intermediate → Advanced (Extendable)

Tech Stack:

* Python
* NumPy
* Pandas
* Paho MQTT
* FPDF2
* Pytest
* Requests
* Python Dotenv
* Matplotlib
* Home Assistant
* Grafana
* MQTT

Use Cases:

* Smart Home Energy Monitoring
* Building Energy Analytics
* IoT Coursework and Academic Projects
* MQTT Communication Demonstrations
* Energy Cost Optimization Studies
* Virtual Hardware Simulation
* Embedded Systems Prototyping
* Dashboard and Automation Testing

Project Workflow:
Appliance Profiles
↓
Energy Simulator
↓
Power & Energy Analytics
↓
Cost Estimation
↓
Alert Engine
↓
CSV / PDF Reporting
↓
MQTT Publishing
↓
Dashboard Visualization

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

__version__ = "1.0.0"
__author__ = "Akash Das"
