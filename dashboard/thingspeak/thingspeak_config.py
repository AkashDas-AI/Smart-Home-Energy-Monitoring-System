"""
ThingSpeak Configuration
========================

Configuration settings for publishing Smart Home Energy
Monitoring telemetry data to a ThingSpeak channel.

Author: Akash Das
Project: Smart Home Energy Monitoring System
Version: 1.0.0
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# ==========================================================
# ThingSpeak Credentials
# ==========================================================

# Replace with your actual ThingSpeak Channel ID
THINGSPEAK_CHANNEL_ID = os.getenv(
    "THINGSPEAK_CHANNEL_ID",
    "YOUR_CHANNEL_ID"
)

# Replace with your actual ThingSpeak Write API Key
THINGSPEAK_API_KEY = os.getenv(
    "THINGSPEAK_API_KEY",
    "YOUR_WRITE_API_KEY"
)

# ==========================================================
# API Endpoint
# ==========================================================

THINGSPEAK_UPDATE_URL = (
    "https://api.thingspeak.com/update"
)

# ==========================================================
# Update Settings
# ==========================================================

# ThingSpeak free accounts allow updates
# approximately every 15 seconds.
UPDATE_INTERVAL_SECONDS = 15

# ==========================================================
# Field Mapping
# ==========================================================

FIELD_MAPPING = {
    "voltage": "field1",
    "current": "field2",
    "active_power": "field3",
    "energy_kwh": "field4",
    "estimated_cost": "field5",
    "power_factor": "field6",
    "alert_count": "field7",
    "system_status": "field8",
}

# ==========================================================
# Validation Helper
# ==========================================================

def validate_configuration() -> bool:
    """
    Validate ThingSpeak configuration.

    Returns:
        bool: True if configuration appears valid.
    """
    return (
        THINGSPEAK_CHANNEL_ID not in (
            "", "YOUR_CHANNEL_ID"
        )
        and
        THINGSPEAK_API_KEY not in (
            "", "YOUR_WRITE_API_KEY"
        )
    )


# ==========================================================
# Example .env Entries
# ==========================================================
#
# THINGSPEAK_CHANNEL_ID=1234567
# THINGSPEAK_API_KEY=ABCDEFG123456789
#
# ==========================================================