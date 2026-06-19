"""
Smart Home Energy Monitoring System - Power Calculator.

This module contains electrical power calculation utilities used by the
energy monitoring simulator.

The calculations implemented here mirror the concepts used in real-world
energy monitoring systems, smart meters, industrial energy analyzers,
and building energy management platforms.

Electrical Metrics:
-------------------
1. Apparent Power (S)
   S = V × I
   Unit: Volt-Amperes (VA)

2. Active Power (P)
   P = V × I × PF
   Unit: Watts (W)

3. Reactive Power (Q)
   Q = √(S² - P²)
   Unit: Volt-Ampere Reactive (VAR)

4. Power Factor (PF)
   PF = P / S

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from math import sqrt
from typing import Dict


class PowerCalculator:
    """
    Utility class for electrical power calculations.
    """

    @staticmethod
    def calculate_apparent_power(
        voltage: float,
        current: float
    ) -> float:
        """
        Calculate Apparent Power (VA).

        Formula:
            S = V × I

        Parameters
        ----------
        voltage : float
            Voltage in Volts.

        current : float
            Current in Amperes.

        Returns
        -------
        float
            Apparent Power (VA)
        """

        return round(voltage * current, 2)

    @staticmethod
    def calculate_active_power(
        voltage: float,
        current: float,
        power_factor: float
    ) -> float:
        """
        Calculate Active Power (W).

        Formula:
            P = V × I × PF

        Parameters
        ----------
        voltage : float

        current : float

        power_factor : float

        Returns
        -------
        float
            Active Power (W)
        """

        return round(
            voltage * current * power_factor,
            2
        )

    @staticmethod
    def calculate_reactive_power(
        apparent_power: float,
        active_power: float
    ) -> float:
        """
        Calculate Reactive Power (VAR).

        Formula:
            Q = √(S² - P²)

        Parameters
        ----------
        apparent_power : float

        active_power : float

        Returns
        -------
        float
            Reactive Power (VAR)
        """

        reactive = sqrt(
            max(
                (apparent_power ** 2) -
                (active_power ** 2),
                0
            )
        )

        return round(reactive, 2)

    @staticmethod
    def calculate_power_factor(
        active_power: float,
        apparent_power: float
    ) -> float:
        """
        Calculate Power Factor.

        Formula:
            PF = P / S

        Parameters
        ----------
        active_power : float

        apparent_power : float

        Returns
        -------
        float
            Power Factor
        """

        if apparent_power <= 0:
            return 0.0

        return round(
            active_power / apparent_power,
            3
        )

    @classmethod
    def calculate_all_metrics(
        cls,
        voltage: float,
        current: float,
        power_factor: float
    ) -> Dict[str, float]:
        """
        Calculate all power metrics at once.

        Parameters
        ----------
        voltage : float

        current : float

        power_factor : float

        Returns
        -------
        dict
            Complete power metrics payload.
        """

        apparent_power = cls.calculate_apparent_power(
            voltage,
            current
        )

        active_power = cls.calculate_active_power(
            voltage,
            current,
            power_factor
        )

        reactive_power = cls.calculate_reactive_power(
            apparent_power,
            active_power
        )

        calculated_pf = cls.calculate_power_factor(
            active_power,
            apparent_power
        )

        return {
            "voltage": round(voltage, 2),
            "current": round(current, 3),
            "apparent_power_va": apparent_power,
            "active_power_w": active_power,
            "reactive_power_var": reactive_power,
            "power_factor": calculated_pf
        }


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def calculate_apparent_power(
    voltage: float,
    current: float
) -> float:
    """
    Functional wrapper for apparent power.
    """

    return PowerCalculator.calculate_apparent_power(
        voltage,
        current
    )


def calculate_active_power(
    voltage: float,
    current: float,
    power_factor: float
) -> float:
    """
    Functional wrapper for active power.
    """

    return PowerCalculator.calculate_active_power(
        voltage,
        current,
        power_factor
    )


def calculate_reactive_power(
    apparent_power: float,
    active_power: float
) -> float:
    """
    Functional wrapper for reactive power.
    """

    return PowerCalculator.calculate_reactive_power(
        apparent_power,
        active_power
    )


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    sample_voltage = 230.0
    sample_current = 4.5
    sample_pf = 0.92

    results = PowerCalculator.calculate_all_metrics(
        voltage=sample_voltage,
        current=sample_current,
        power_factor=sample_pf
    )

    print("\nPower Calculation Results\n")

    for key, value in results.items():
        print(f"{key}: {value}")