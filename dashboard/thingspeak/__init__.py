"""
ThingSpeak Integration Package
==============================

Provides configuration and API communication utilities
for publishing Smart Home Energy Monitoring telemetry
to ThingSpeak channels.

Modules:
--------
- thingspeak_config
- thingspeak_client

Author: Akash Das
Project: Smart Home Energy Monitoring System
Version: 1.0.0
"""

__version__ = "1.0.0"
__author__ = "Akash Das"

from .thingspeak_config import (
    THINGSPEAK_API_KEY,
    THINGSPEAK_CHANNEL_ID,
    THINGSPEAK_UPDATE_URL,
)

from .thingspeak_client import ThingSpeakClient

__all__ = [
    "ThingSpeakClient",
    "THINGSPEAK_API_KEY",
    "THINGSPEAK_CHANNEL_ID",
    "THINGSPEAK_UPDATE_URL",
]