# Smart Home Energy Monitoring System

## Project Overview

The Smart Home Energy Monitoring System is an Internet of Things (IoT) project designed to monitor, analyze, and visualize household electricity consumption in real time. The system enables homeowners to track power usage, identify energy-intensive appliances, receive safety alerts, and estimate electricity costs through a centralized monitoring platform.

The project is intentionally designed using a dual-track architecture:

### Physical Track

A real-world implementation using:

- ESP32 Microcontroller
- SCT-013 Current Clamp Sensor
- Voltage Sensor Module
- MQTT Communication
- Home Assistant
- Grafana Dashboards

This track demonstrates how energy monitoring systems are deployed in modern smart homes and industrial IoT environments.

### Virtual Track

A complete software simulation that mimics the behavior of the physical hardware.

The Python simulator generates realistic electrical measurements and publishes them through MQTT using the exact payload structure expected from the ESP32 firmware. This allows the entire system to run without physical hardware while maintaining full compatibility with the production architecture.

This approach ensures that:

- Recruiters can run the project locally
- Developers can test the system without hardware
- The architecture remains hardware-ready for deployment

---

# Problem Statement

Residential electricity consumption is often difficult to monitor at the appliance level. Most consumers only receive periodic utility bills without visibility into real-time usage patterns.

This creates several challenges:

- Energy wastage goes unnoticed
- High-consumption appliances are difficult to identify
- Safety issues such as overloads and overcurrent conditions may remain undetected
- Cost forecasting becomes difficult

The Smart Home Energy Monitoring System addresses these challenges by providing continuous monitoring, analytics, alerting, and visualization capabilities.

---

# Project Objectives

The primary objectives of the project are:

- Monitor voltage and current measurements in real time
- Calculate active, reactive, and apparent power
- Track cumulative energy consumption (kWh)
- Estimate electricity costs using configurable tariffs
- Detect abnormal electrical conditions
- Generate automated reports
- Publish telemetry through MQTT
- Integrate with Home Assistant
- Visualize metrics using Grafana
- Support both simulated and physical deployments

---

# Key Features

## Real-Time Monitoring

The system continuously monitors:

- Voltage (V)
- Current (A)
- Power Factor
- Active Power (W)
- Reactive Power (VAR)
- Apparent Power (VA)
- Energy Consumption (kWh)

---

## Cost Estimation

The platform calculates:

- Running electricity costs
- Daily consumption estimates
- Monthly consumption estimates
- Tariff-based billing projections

---

## Alert System

Safety monitoring includes:

- Overvoltage Detection
- Undervoltage Detection
- Overcurrent Detection
- Power Overload Detection
- High Energy Usage Alerts

---

## MQTT-Based Communication

All telemetry data is transmitted through MQTT topics, enabling:

- Lightweight communication
- Real-time updates
- Easy integration with IoT platforms
- Cloud-ready architecture

---

## Home Assistant Integration

Home Assistant provides:

- Smart home compatibility
- MQTT entity management
- Automation support
- Notification workflows

---

## Grafana Dashboard

Grafana is used to visualize:

- Live power usage
- Energy trends
- Cost analytics
- Alert statistics
- Historical consumption patterns

---

## Automated Reporting

The system generates:

- CSV Telemetry Logs
- Daily Energy Reports
- Monthly Usage Reports
- PDF Summaries

---

# System Architecture

```text
                 ┌─────────────────────┐
                 │ ESP32 Hardware Node │
                 └──────────┬──────────┘
                            │
                            │ MQTT
                            │
                            ▼

                 ┌────────────────────┐
                 │  MQTT Broker       │
                 │   (Mosquitto)      │
                 └──────────┬─────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼

     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │ Simulator  │  │ Home       │  │ Reporting  │
     │ (Python)   │  │ Assistant  │  │ Engine     │
     └─────┬──────┘  └─────┬──────┘  └────────────┘
           │               │
           ▼               ▼

      ┌─────────────────────────┐
      │         Grafana         │
      │  Dashboards & Analytics │
      └─────────────────────────┘
```

---

# Technology Stack

## Programming Languages

- Python
- C++
- Arduino Framework

---

## IoT & Communication

- MQTT
- Mosquitto Broker

---

## Embedded Systems

- ESP32
- SCT-013 Current Sensor
- Voltage Sensor Module

---

## Data Processing

- NumPy
- Pandas

---

## Reporting

- CSV
- PDF (FPDF2)

---

## Dashboard & Visualization

- Home Assistant
- Grafana

---

## Testing

- Pytest
- Pytest-Cov

---

## Version Control

- Git
- GitHub

---

# Project Structure

The repository is organized into several major modules:

| Module | Purpose |
|----------|----------|
| firmware | ESP32 firmware implementation |
| simulator | Virtual smart meter implementation |
| dashboard | Home Assistant and Grafana configurations |
| mqtt | MQTT documentation and payload definitions |
| reports | Generated reports |
| outputs | Runtime exports and logs |
| docs | Technical documentation |
| tests | Unit testing suite |
| deployment | Docker deployment configurations |

---

# Industry Relevance

This project mirrors modern IoT energy monitoring architectures commonly found in:

- Smart Homes
- Building Automation Systems
- Industrial Energy Monitoring
- Smart Grid Applications
- Facility Management Platforms
- Utility Analytics Systems

The architecture demonstrates practical experience with embedded systems, IoT communication protocols, telemetry pipelines, monitoring dashboards, and data analytics workflows.

---

# Learning Outcomes

Through this project, developers gain hands-on experience in:

- Internet of Things (IoT)
- MQTT Messaging
- Embedded Systems Development
- ESP32 Programming
- Real-Time Data Streaming
- Energy Analytics
- Home Assistant Integration
- Grafana Dashboard Development
- Python System Design
- Technical Documentation
- Software Testing

---

# Author

**Akash Das**

Project:
**Smart Home Energy Monitoring System**

Version:
**1.0.0**