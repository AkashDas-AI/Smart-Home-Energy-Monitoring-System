"""
Smart Home Energy Monitoring System - Energy Simulator.

This module serves as the virtual smart meter for the project.

It generates realistic electrical telemetry by selecting appliance
profiles and simulating their operating characteristics.

The generated output mimics the data that would normally be received
from an ESP32 connected to:

- ACS712 Current Sensor
- Voltage Sensor Module
- Smart Energy Meter Hardware

Generated Metrics:
------------------
- Voltage (V)
- Current (A)
- Apparent Power (VA)
- Active Power (W)
- Reactive Power (VAR)
- Power Factor
- Energy Consumption (kWh)
- Estimated Cost
- Alert Status

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from datetime import datetime
from typing import Dict
import random

from simulator.core.config import (
    DEVICE_ID,
    LOCATION,
    ENABLE_RANDOM_NOISE,
    NOISE_PERCENTAGE
)

from simulator.core.appliance_profiles import (
    get_random_appliance
)

from simulator.analytics.power_calculator import (
    PowerCalculator
)


# ==========================================================
# ENERGY SIMULATOR
# ==========================================================

class EnergySimulator:
    """
    Virtual smart energy meter.
    """

    def __init__(self):
        """
        Initialize simulator.
        """

        self.device_id = DEVICE_ID
        self.location = LOCATION

    # ======================================================
    # INTERNAL HELPERS
    # ======================================================

    @staticmethod
    def apply_noise(
        value: float
    ) -> float:
        """
        Apply random measurement noise.

        Returns
        -------
        float
        """

        if not ENABLE_RANDOM_NOISE:
            return value

        variation = random.uniform(
            -NOISE_PERCENTAGE,
            NOISE_PERCENTAGE
        )

        return value * (1 + variation)

    # ======================================================
    # SIMULATION ENGINE
    # ======================================================

    def generate_measurement(
        self
    ) -> Dict:
        """
        Generate a single telemetry sample.

        Returns
        -------
        dict
        """

        appliance = get_random_appliance()

        appliance_data = (
            appliance.generate_sample()
        )

        voltage = self.apply_noise(
            appliance_data["voltage"]
        )

        current = self.apply_noise(
            appliance_data["current"]
        )

        power_factor = (
            appliance_data["power_factor"]
        )

        metrics = (
            PowerCalculator
            .calculate_all_metrics(
                voltage=voltage,
                current=current,
                power_factor=power_factor
            )
        )

        telemetry = {
            "device_id":
                self.device_id,

            "location":
                self.location,

            "timestamp":
                datetime.now().isoformat(),

            "appliance":
                appliance_data["name"],

            "category":
                appliance_data["category"],

            "is_active":
                appliance_data["is_active"],

            "voltage":
                metrics["voltage"],

            "current":
                metrics["current"],

            "apparent_power_va":
                metrics[
                    "apparent_power_va"
                ],

            "active_power_w":
                metrics[
                    "active_power_w"
                ],

            "reactive_power_var":
                metrics[
                    "reactive_power_var"
                ],

            "power_factor":
                metrics[
                    "power_factor"
                ]
        }

        return telemetry

    def generate_batch(
        self,
        sample_count: int = 10
    ):
        """
        Generate multiple telemetry records.

        Parameters
        ----------
        sample_count : int

        Returns
        -------
        list
        """

        return [
            self.generate_measurement()
            for _ in range(sample_count)
        ]

    def get_device_info(
        self
    ) -> Dict:
        """
        Return simulator metadata.
        """

        return {
            "device_id":
                self.device_id,

            "location":
                self.location,

            "simulation_mode":
                True,

            "virtual_device":
                True
        }


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def generate_sample() -> Dict:
    """
    Generate a single telemetry sample.
    """

    simulator = EnergySimulator()

    return simulator.generate_measurement()


def generate_samples(
    sample_count: int = 10
):
    """
    Generate multiple telemetry samples.
    """

    simulator = EnergySimulator()

    return simulator.generate_batch(
        sample_count
    )


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    simulator = EnergySimulator()

    print(
        "\nSmart Home Energy Simulator\n"
    )

    sample = (
        simulator.generate_measurement()
    )

    print(
        "\nGenerated Telemetry Sample\n"
    )

    for key, value in sample.items():
        print(
            f"{key}: {value}"
        )

    print(
        "\nBatch Generation Example\n"
    )

    samples = simulator.generate_batch(
        sample_count=3
    )

    print(
        f"Generated {len(samples)} samples."
    )