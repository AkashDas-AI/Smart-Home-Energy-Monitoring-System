"""
Smart Home Energy Monitoring System - Communication Package.

This package contains all networking and message transport modules used
by the Smart Home Energy Monitoring System.

The communication layer is responsible for transmitting telemetry,
analytics, alerts, and system status information between the simulator,
ESP32 devices, MQTT brokers, dashboards, and external services.

Core Responsibilities:
- MQTT publishing
- MQTT topic management
- Payload serialization
- JSON message formatting
- Network communication abstraction
- Future API integrations

Modules:
- mqtt_publisher.py
    Handles MQTT client initialization, broker connectivity,
    topic publishing, payload serialization, and connection
    lifecycle management.

Communication Workflow:
Appliance Simulation
        ↓
Analytics Engine
        ↓
Alert Engine
        ↓
Communication Layer
        ↓
MQTT Broker
        ↓
Grafana / Home Assistant / Dashboards

Supported Data Types:
- Sensor Telemetry
- Power Metrics
- Energy Consumption
- Cost Estimates
- Alert Notifications
- Device Status Updates

Design Goals:
- Decoupled network architecture
- Reusable communication interfaces
- Broker-independent implementation
- JSON-based message transport
- Easy migration to cloud platforms

Future Extensions:
- REST API Clients
- WebSocket Streaming
- Cloud IoT Platforms
- Azure IoT Hub
- AWS IoT Core
- Google Cloud IoT

This package intentionally focuses only on message transport and does
not perform simulation, analytics, reporting, or business logic.

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

__all__ = [
    "mqtt_publisher"
]