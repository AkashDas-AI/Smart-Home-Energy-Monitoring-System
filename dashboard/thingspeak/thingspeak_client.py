"""
ThingSpeak Client
=================

Handles communication between the Smart Home Energy
Monitoring System and ThingSpeak using the REST API.

Author: Akash Das
Project: Smart Home Energy Monitoring System
Version: 1.0.0
"""

from __future__ import annotations

import logging
from typing import Any, Dict

import requests

from .thingspeak_config import (
    THINGSPEAK_API_KEY,
    THINGSPEAK_UPDATE_URL,
    FIELD_MAPPING,
)

logger = logging.getLogger(__name__)


class ThingSpeakClient:
    """
    ThingSpeak API Client.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or THINGSPEAK_API_KEY

    def _build_payload(
        self,
        telemetry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Convert simulator telemetry into
        ThingSpeak field payload.

        Parameters
        ----------
        telemetry : dict
            Energy monitoring telemetry.

        Returns
        -------
        dict
            ThingSpeak-compatible payload.
        """

        payload = {
            "api_key": self.api_key
        }

        if "voltage" in telemetry:
            payload[FIELD_MAPPING["voltage"]] = round(
                float(telemetry["voltage"]), 2
            )

        if "current" in telemetry:
            payload[FIELD_MAPPING["current"]] = round(
                float(telemetry["current"]), 2
            )

        if "active_power" in telemetry:
            payload[FIELD_MAPPING["active_power"]] = round(
                float(telemetry["active_power"]), 2
            )

        elif "power" in telemetry:
            payload[FIELD_MAPPING["active_power"]] = round(
                float(telemetry["power"]), 2
            )

        if "energy_kwh" in telemetry:
            payload[FIELD_MAPPING["energy_kwh"]] = round(
                float(telemetry["energy_kwh"]), 4
            )

        if "estimated_cost" in telemetry:
            payload[FIELD_MAPPING["estimated_cost"]] = round(
                float(telemetry["estimated_cost"]), 2
            )

        if "power_factor" in telemetry:
            payload[FIELD_MAPPING["power_factor"]] = round(
                float(telemetry["power_factor"]), 2
            )

        if "alert_count" in telemetry:
            payload[FIELD_MAPPING["alert_count"]] = int(
                telemetry["alert_count"]
            )

        if "system_status" in telemetry:
            payload[FIELD_MAPPING["system_status"]] = str(
                telemetry["system_status"]
            )

        return payload

    def publish(
        self,
        telemetry: Dict[str, Any]
    ) -> bool:
        """
        Publish telemetry to ThingSpeak.

        Parameters
        ----------
        telemetry : dict
            Telemetry data.

        Returns
        -------
        bool
            True if successful.
        """

        try:
            payload = self._build_payload(
                telemetry
            )

            response = requests.post(
                THINGSPEAK_UPDATE_URL,
                data=payload,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(
                    "ThingSpeak update successful."
                )
                return True

            logger.warning(
                "ThingSpeak returned status %s",
                response.status_code
            )

            return False

        except requests.RequestException as exc:
            logger.error(
                "ThingSpeak connection error: %s",
                exc
            )
            return False

        except Exception as exc:
            logger.error(
                "ThingSpeak publish error: %s",
                exc
            )
            return False

    def publish_energy_data(
        self,
        voltage: float,
        current: float,
        power: float,
        energy_kwh: float,
        cost: float,
        power_factor: float,
        alert_count: int = 0,
        status: str = "ONLINE",
    ) -> bool:
        """
        Convenience helper for publishing
        energy monitoring data.
        """

        telemetry = {
            "voltage": voltage,
            "current": current,
            "active_power": power,
            "energy_kwh": energy_kwh,
            "estimated_cost": cost,
            "power_factor": power_factor,
            "alert_count": alert_count,
            "system_status": status,
        }

        return self.publish(telemetry)

    def test_connection(self) -> bool:
        """
        Send a simple test update to verify
        ThingSpeak connectivity.
        """

        test_payload = {
            "voltage": 230,
            "current": 5,
            "active_power": 1150,
            "energy_kwh": 1.0,
            "estimated_cost": 8.0,
            "power_factor": 0.95,
            "alert_count": 0,
            "system_status": "ONLINE",
        }

        return self.publish(test_payload)