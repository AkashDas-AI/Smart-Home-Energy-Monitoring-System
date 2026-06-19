"""
Unit Tests - MQTT Publisher

This test suite validates the MQTT communication layer used by the
Smart Home Energy Monitoring System.

NOTE:
------
These tests focus primarily on object initialization,
payload generation, serialization, and helper methods.

A real MQTT broker is NOT required for most tests.

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

import json
import pytest

from simulator.communication.mqtt_publisher import (
    MQTTPublisher,
    DEVICE_ID
)


# ==========================================================
# INITIALIZATION TESTS
# ==========================================================

def test_mqtt_publisher_initialization():
    """
    Verify publisher initializes correctly.
    """

    publisher = MQTTPublisher()

    assert publisher.broker is not None
    assert publisher.port > 0
    assert publisher.topic is not None

    assert publisher.connected is False


# ==========================================================
# PAYLOAD SERIALIZATION TESTS
# ==========================================================

def test_payload_serialization():
    """
    Verify JSON serialization.
    """

    payload = {
        "device_id": "SIM_NODE_001",
        "voltage": 230,
        "current": 5
    }

    serialized = (
        MQTTPublisher.serialize_payload(
            payload
        )
    )

    assert isinstance(
        serialized,
        str
    )

    deserialized = json.loads(
        serialized
    )

    assert (
        deserialized["device_id"]
        == "SIM_NODE_001"
    )

    assert (
        deserialized["voltage"]
        == 230
    )


# ==========================================================
# STATUS PAYLOAD TESTS
# ==========================================================

def test_status_payload_generation():
    """
    Verify status payload creation.
    """

    payload = (
        MQTTPublisher
        .build_status_payload(
            "ONLINE"
        )
    )

    assert (
        payload["device_id"]
        == DEVICE_ID
    )

    assert (
        payload["status"]
        == "ONLINE"
    )

    assert (
        "timestamp"
        in payload
    )


def test_offline_status_payload():
    """
    Verify OFFLINE payload.
    """

    payload = (
        MQTTPublisher
        .build_status_payload(
            "OFFLINE"
        )
    )

    assert (
        payload["status"]
        == "OFFLINE"
    )


# ==========================================================
# TELEMETRY PAYLOAD TESTS
# ==========================================================

def test_telemetry_payload_structure():
    """
    Validate a typical telemetry payload.
    """

    payload = {
        "device_id":
            DEVICE_ID,

        "voltage":
            230.5,

        "current":
            4.2,

        "active_power_w":
            890.3,

        "energy_kwh":
            1.25
    }

    serialized = (
        MQTTPublisher
        .serialize_payload(
            payload
        )
    )

    decoded = json.loads(
        serialized
    )

    assert (
        decoded["device_id"]
        == DEVICE_ID
    )

    assert (
        "active_power_w"
        in decoded
    )

    assert (
        "energy_kwh"
        in decoded
    )


# ==========================================================
# CONNECTION TESTS
# ==========================================================

def test_connect_returns_boolean():
    """
    Verify connect() returns bool.

    Connection may fail if broker
    is not running, which is okay.
    """

    publisher = MQTTPublisher()

    result = publisher.connect()

    assert isinstance(
        result,
        bool
    )

    publisher.disconnect()


# ==========================================================
# PUBLISH METHOD TESTS
# ==========================================================

def test_publish_returns_boolean():
    """
    Verify publish() returns bool.
    """

    publisher = MQTTPublisher()

    payload = {
        "message":
            "test"
    }

    result = publisher.publish(
        payload
    )

    assert isinstance(
        result,
        bool
    )

    publisher.disconnect()


def test_publish_telemetry_returns_boolean():
    """
    Verify telemetry publisher.
    """

    publisher = MQTTPublisher()

    payload = {
        "device_id":
            DEVICE_ID,

        "voltage":
            230,

        "current":
            5
    }

    result = (
        publisher
        .publish_telemetry(
            payload
        )
    )

    assert isinstance(
        result,
        bool
    )

    publisher.disconnect()


def test_publish_status_returns_boolean():
    """
    Verify status publisher.
    """

    publisher = MQTTPublisher()

    result = (
        publisher.publish_status(
            "ONLINE"
        )
    )

    assert isinstance(
        result,
        bool
    )

    publisher.disconnect()


# ==========================================================
# EDGE CASE TESTS
# ==========================================================

def test_empty_payload_serialization():
    """
    Verify empty payload handling.
    """

    payload = {}

    serialized = (
        MQTTPublisher
        .serialize_payload(
            payload
        )
    )

    assert serialized == "{}"


def test_large_payload_serialization():
    """
    Verify large payload support.
    """

    payload = {
        "data":
            "X" * 5000
    }

    serialized = (
        MQTTPublisher
        .serialize_payload(
            payload
        )
    )

    assert isinstance(
        serialized,
        str
    )


# ==========================================================
# PYTEST ENTRY
# ==========================================================

if __name__ == "__main__":
    pytest.main()