"""
Smart Home Energy Monitoring System - MQTT Publisher.

This module handles MQTT communication between the simulator and
external systems such as:

- Home Assistant
- Grafana
- InfluxDB
- Node-RED
- Cloud IoT Platforms
- MQTT Explorer

Responsibilities:
-----------------
- Establish broker connection
- Publish telemetry payloads
- Publish alert messages
- Publish device status updates
- Serialize data into JSON
- Manage MQTT lifecycle

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

import json
from datetime import datetime
from typing import Dict, Optional

import paho.mqtt.client as mqtt  # type: ignore[import]

from simulator.core.config import (
    MQTT_BROKER,
    MQTT_PORT,
    MQTT_KEEPALIVE,
    MQTT_TOPIC,
    MQTT_CLIENT_ID,
    DEVICE_ID
)


# ==========================================================
# MQTT PUBLISHER
# ==========================================================

class MQTTPublisher:
    """
    MQTT communication manager.
    """

    def __init__(
        self,
        broker: str = MQTT_BROKER,
        port: int = MQTT_PORT,
        topic: str = MQTT_TOPIC
    ):
        """
        Initialize MQTT publisher.
        """

        self.broker = broker
        self.port = port
        self.topic = topic

        self.connected = False

        self.client = mqtt.Client(
            callback_api_version=
            mqtt.CallbackAPIVersion.VERSION2,
            client_id=MQTT_CLIENT_ID
        )

        self.client.on_connect = (
            self._on_connect
        )

        self.client.on_disconnect = (
            self._on_disconnect
        )

    # ======================================================
    # MQTT CALLBACKS
    # ======================================================

    def _on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties
    ):
        """
        MQTT connection callback.
        """

        if reason_code == 0:

            self.connected = True

            print(
                f"[MQTT] Connected to "
                f"{self.broker}:{self.port}"
            )

        else:

            print(
                f"[MQTT] Connection failed "
                f"(code={reason_code})"
            )

    def _on_disconnect(
        self,
        client,
        userdata,
        disconnect_flags,
        reason_code,
        properties
    ):
        """
        MQTT disconnect callback.
        """

        self.connected = False

        print(
            f"[MQTT] Disconnected "
            f"(code={reason_code})"
        )

    # ======================================================
    # CONNECTION MANAGEMENT
    # ======================================================

    def connect(self) -> bool:
        """
        Connect to MQTT broker.
        """

        try:

            self.client.connect(
                host=self.broker,
                port=self.port,
                keepalive=MQTT_KEEPALIVE
            )

            self.client.loop_start()

            return True

        except Exception as error:

            print(
                f"[MQTT] Connection Error: "
                f"{error}"
            )

            return False

    def disconnect(self):
        """
        Disconnect MQTT client.
        """

        try:

            self.client.loop_stop()

            self.client.disconnect()

        except Exception as error:

            print(
                f"[MQTT] Disconnect Error: "
                f"{error}"
            )

    # ======================================================
    # PAYLOAD HELPERS
    # ======================================================

    @staticmethod
    def serialize_payload(
        payload: Dict
    ) -> str:
        """
        Convert payload to JSON string.
        """

        return json.dumps(
            payload,
            indent=None,
            default=str
        )

    @staticmethod
    def build_status_payload(
        status: str
    ) -> Dict:
        """
        Create device status payload.
        """

        return {
            "device_id": DEVICE_ID,
            "timestamp":
                datetime.now().isoformat(),
            "status": status
        }

    # ======================================================
    # PUBLISH METHODS
    # ======================================================

    def publish(
        self,
        payload: Dict,
        topic: Optional[str] = None,
        qos: int = 0,
        retain: bool = False
    ) -> bool:
        """
        Publish JSON payload.
        """

        publish_topic = (
            topic if topic else self.topic
        )

        try:

            payload_json = (
                self.serialize_payload(
                    payload
                )
            )

            result = self.client.publish(
                topic=publish_topic,
                payload=payload_json,
                qos=qos,
                retain=retain
            )

            return (
                result.rc ==
                mqtt.MQTT_ERR_SUCCESS
            )

        except Exception as error:

            print(
                f"[MQTT] Publish Error: "
                f"{error}"
            )

            return False

    def publish_telemetry(
        self,
        telemetry_payload: Dict
    ) -> bool:
        """
        Publish energy telemetry.
        """

        topic = (
            f"{self.topic}/telemetry"
        )

        return self.publish(
            payload=telemetry_payload,
            topic=topic
        )

    def publish_alert(
        self,
        alert_payload: Dict
    ) -> bool:
        """
        Publish alert event.
        """

        topic = (
            f"{self.topic}/alerts"
        )

        return self.publish(
            payload=alert_payload,
            topic=topic
        )

    def publish_status(
        self,
        status: str
    ) -> bool:
        """
        Publish simulator status.
        """

        topic = (
            f"{self.topic}/status"
        )

        payload = (
            self.build_status_payload(
                status
            )
        )

        return self.publish(
            payload=payload,
            topic=topic,
            retain=True
        )


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def publish_payload(
    payload: Dict
) -> bool:
    """
    Quick publish helper.
    """

    publisher = MQTTPublisher()

    if not publisher.connect():
        return False

    success = publisher.publish(
        payload
    )

    publisher.disconnect()

    return success


def publish_telemetry(
    telemetry_payload: Dict
) -> bool:
    """
    Quick telemetry publish helper.
    """

    publisher = MQTTPublisher()

    if not publisher.connect():
        return False

    success = publisher.publish_telemetry(
        telemetry_payload
    )

    publisher.disconnect()

    return success


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    publisher = MQTTPublisher()

    if publisher.connect():

        sample_payload = {
            "device_id": DEVICE_ID,
            "timestamp":
                datetime.now().isoformat(),
            "voltage": 230.4,
            "current": 3.2,
            "active_power_w": 670.8,
            "energy_kwh": 1.58,
            "cost": 13.43,
            "alert_status": "NORMAL"
        }

        publisher.publish_telemetry(
            sample_payload
        )

        publisher.publish_status(
            "ONLINE"
        )

        print(
            "\nSample payload published."
        )

        publisher.disconnect()

    else:

        print(
            "\nUnable to connect "
            "to MQTT broker."
        )