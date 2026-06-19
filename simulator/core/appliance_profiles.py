"""
Smart Home Energy Monitoring System - Appliance Profiles Module.

This module defines realistic household appliance profiles used by the
energy simulator to generate synthetic electrical telemetry.

Each appliance profile contains:

- Voltage range
- Current range
- Active power range
- Power factor
- Typical operating pattern
- Category information

The goal is to mimic realistic appliance behavior found in modern homes
so that energy analytics, alerts, reporting, and dashboards operate on
plausible data.

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from dataclasses import dataclass
from typing import Dict
import random

from simulator.core.config import (
    NOMINAL_VOLTAGE,
    MIN_VOLTAGE,
    MAX_VOLTAGE
)


# ==========================================================
# APPLIANCE DATA MODEL
# ==========================================================

@dataclass
class ApplianceProfile:
    """
    Represents a realistic appliance profile.

    Attributes
    ----------
    name : str
        Appliance name.

    category : str
        Appliance category.

    min_power : float
        Minimum active power (W).

    max_power : float
        Maximum active power (W).

    power_factor : float
        Typical operating power factor.

    duty_cycle : float
        Probability of appliance being active.
        Value between 0 and 1.
    """

    name: str
    category: str

    min_power: float
    max_power: float

    power_factor: float

    duty_cycle: float

    def generate_sample(self) -> Dict:
        """
        Generate a simulated telemetry sample.

        Returns
        -------
        dict
            Simulated appliance electrical values.
        """

        voltage = round(
            random.uniform(
                MIN_VOLTAGE,
                MAX_VOLTAGE
            ),
            2
        )

        active_power = round(
            random.uniform(
                self.min_power,
                self.max_power
            ),
            2
        )

        current = round(
            active_power /
            (voltage * self.power_factor),
            3
        )

        return {
            "name": self.name,
            "category": self.category,
            "voltage": voltage,
            "current": current,
            "power": active_power,
            "power_factor": self.power_factor,
            "is_active": random.random() < self.duty_cycle
        }


# ==========================================================
# APPLIANCE LIBRARY
# ==========================================================

APPLIANCES = {

    # ------------------------------------------------------
    # Lighting
    # ------------------------------------------------------

    "led_bulb": ApplianceProfile(
        name="LED Bulb",
        category="Lighting",
        min_power=5,
        max_power=15,
        power_factor=0.95,
        duty_cycle=0.70
    ),

    "tube_light": ApplianceProfile(
        name="Tube Light",
        category="Lighting",
        min_power=18,
        max_power=40,
        power_factor=0.92,
        duty_cycle=0.65
    ),

    # ------------------------------------------------------
    # Cooling
    # ------------------------------------------------------

    "ceiling_fan": ApplianceProfile(
        name="Ceiling Fan",
        category="Cooling",
        min_power=50,
        max_power=90,
        power_factor=0.90,
        duty_cycle=0.60
    ),

    "air_conditioner": ApplianceProfile(
        name="Air Conditioner",
        category="Cooling",
        min_power=1000,
        max_power=2200,
        power_factor=0.88,
        duty_cycle=0.45
    ),

    # ------------------------------------------------------
    # Kitchen
    # ------------------------------------------------------

    "refrigerator": ApplianceProfile(
        name="Refrigerator",
        category="Kitchen",
        min_power=120,
        max_power=300,
        power_factor=0.85,
        duty_cycle=0.90
    ),

    "induction_cooktop": ApplianceProfile(
        name="Induction Cooktop",
        category="Kitchen",
        min_power=1000,
        max_power=2200,
        power_factor=0.98,
        duty_cycle=0.25
    ),

    "microwave": ApplianceProfile(
        name="Microwave Oven",
        category="Kitchen",
        min_power=700,
        max_power=1500,
        power_factor=0.95,
        duty_cycle=0.10
    ),

    # ------------------------------------------------------
    # Entertainment
    # ------------------------------------------------------

    "television": ApplianceProfile(
        name="Television",
        category="Entertainment",
        min_power=50,
        max_power=180,
        power_factor=0.95,
        duty_cycle=0.40
    ),

    "gaming_console": ApplianceProfile(
        name="Gaming Console",
        category="Entertainment",
        min_power=100,
        max_power=250,
        power_factor=0.96,
        duty_cycle=0.15
    ),

    # ------------------------------------------------------
    # Utility
    # ------------------------------------------------------

    "washing_machine": ApplianceProfile(
        name="Washing Machine",
        category="Utility",
        min_power=500,
        max_power=1200,
        power_factor=0.82,
        duty_cycle=0.15
    ),

    "water_pump": ApplianceProfile(
        name="Water Pump",
        category="Utility",
        min_power=500,
        max_power=1500,
        power_factor=0.80,
        duty_cycle=0.10
    ),

    "wifi_router": ApplianceProfile(
        name="Wi-Fi Router",
        category="Networking",
        min_power=8,
        max_power=20,
        power_factor=0.97,
        duty_cycle=1.00
    ),

    "laptop": ApplianceProfile(
        name="Laptop",
        category="Computing",
        min_power=40,
        max_power=120,
        power_factor=0.98,
        duty_cycle=0.50
    )
}


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_appliance(name: str) -> ApplianceProfile:
    """
    Retrieve appliance profile by key.

    Parameters
    ----------
    name : str

    Returns
    -------
    ApplianceProfile
    """

    return APPLIANCES[name]


def get_random_appliance() -> ApplianceProfile:
    """
    Select a random appliance profile.

    Returns
    -------
    ApplianceProfile
    """

    return random.choice(
        list(APPLIANCES.values())
    )


def list_appliances():
    """
    List all available appliance keys.
    """

    return list(APPLIANCES.keys())


def appliance_count() -> int:
    """
    Total appliance profiles available.
    """

    return len(APPLIANCES)


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    print("\nAvailable Appliances\n")

    for appliance_name in list_appliances():
        print(f"• {appliance_name}")

    print("\nRandom Sample\n")

    sample = get_random_appliance().generate_sample()

    for key, value in sample.items():
        print(f"{key}: {value}")