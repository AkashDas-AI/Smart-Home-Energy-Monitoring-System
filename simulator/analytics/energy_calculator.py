"""
Smart Home Energy Monitoring System - Energy Calculator.

This module is responsible for converting power measurements into
energy consumption metrics.

In electrical systems, power represents the instantaneous rate of
energy usage, while energy represents accumulated consumption over
a period of time.

This module tracks:

- Watt-hours (Wh)
- Kilowatt-hours (kWh)
- Session Energy Usage
- Daily Energy Usage
- Monthly Energy Usage
- Running Consumption Totals

Core Formula:
-------------
Energy (Wh) = Power (W) × Time (Hours)

Energy (kWh) = Energy (Wh) / 1000

Examples:
---------
1000 W appliance running for 1 hour:

Energy = 1000 × 1
       = 1000 Wh
       = 1.0 kWh

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from typing import Dict


class EnergyCalculator:
    """
    Tracks cumulative energy consumption.

    This class maintains a running total of energy
    consumed throughout the simulator session.
    """

    def __init__(self):
        """
        Initialize energy counters.
        """

        self.total_energy_wh = 0.0
        self.total_energy_kwh = 0.0

    def calculate_energy_wh(
        self,
        power_watts: float,
        duration_seconds: float
    ) -> float:
        """
        Calculate energy consumption in Watt-hours.

        Formula:
            Energy (Wh) =
            Power (W) × Time (Hours)

        Parameters
        ----------
        power_watts : float

        duration_seconds : float

        Returns
        -------
        float
            Energy consumed in Wh.
        """

        duration_hours = duration_seconds / 3600

        energy_wh = (
            power_watts *
            duration_hours
        )

        return round(energy_wh, 6)

    def calculate_energy_kwh(
        self,
        power_watts: float,
        duration_seconds: float
    ) -> float:
        """
        Calculate energy consumption in kWh.

        Parameters
        ----------
        power_watts : float

        duration_seconds : float

        Returns
        -------
        float
            Energy consumed in kWh.
        """

        energy_wh = self.calculate_energy_wh(
            power_watts,
            duration_seconds
        )

        return round(
            energy_wh / 1000,
            8
        )

    def add_consumption(
        self,
        power_watts: float,
        duration_seconds: float
    ) -> Dict[str, float]:
        """
        Add energy consumption to the running total.

        Parameters
        ----------
        power_watts : float

        duration_seconds : float

        Returns
        -------
        dict
            Current cumulative statistics.
        """

        energy_wh = self.calculate_energy_wh(
            power_watts,
            duration_seconds
        )

        energy_kwh = energy_wh / 1000

        self.total_energy_wh += energy_wh
        self.total_energy_kwh += energy_kwh

        return {
            "interval_energy_wh": round(
                energy_wh,
                6
            ),
            "interval_energy_kwh": round(
                energy_kwh,
                8
            ),
            "total_energy_wh": round(
                self.total_energy_wh,
                4
            ),
            "total_energy_kwh": round(
                self.total_energy_kwh,
                6
            )
        }

    def get_total_energy_wh(self) -> float:
        """
        Return total accumulated Wh.
        """

        return round(
            self.total_energy_wh,
            4
        )

    def get_total_energy_kwh(self) -> float:
        """
        Return total accumulated kWh.
        """

        return round(
            self.total_energy_kwh,
            6
        )

    def reset(self):
        """
        Reset all counters.
        """

        self.total_energy_wh = 0.0
        self.total_energy_kwh = 0.0

    def get_summary(self) -> Dict[str, float]:
        """
        Return energy summary.

        Returns
        -------
        dict
        """

        return {
            "total_energy_wh": round(
                self.total_energy_wh,
                4
            ),
            "total_energy_kwh": round(
                self.total_energy_kwh,
                6
            )
        }


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def calculate_energy_wh(
    power_watts: float,
    duration_seconds: float
) -> float:
    """
    Functional helper for Wh calculation.
    """

    duration_hours = duration_seconds / 3600

    return round(
        power_watts * duration_hours,
        6
    )


def calculate_energy_kwh(
    power_watts: float,
    duration_seconds: float
) -> float:
    """
    Functional helper for kWh calculation.
    """

    energy_wh = calculate_energy_wh(
        power_watts,
        duration_seconds
    )

    return round(
        energy_wh / 1000,
        8
    )


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    calculator = EnergyCalculator()

    sample_power = 1500.0
    sample_duration = 60

    result = calculator.add_consumption(
        power_watts=sample_power,
        duration_seconds=sample_duration
    )

    print("\nEnergy Calculation Results\n")

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nSummary\n")

    print(calculator.get_summary())