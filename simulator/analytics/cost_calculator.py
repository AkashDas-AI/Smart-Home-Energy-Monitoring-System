"""
Smart Home Energy Monitoring System - Cost Calculator.

This module converts energy consumption metrics into estimated
electricity costs.

The calculator supports:

- Flat tariff billing
- Tiered slab billing
- Daily cost estimation
- Monthly cost estimation
- Running cost accumulation

By default, the simulator uses a flat-rate tariff model because it is
simpler and aligns well with educational and portfolio projects.

Core Formula:
-------------
Cost = Energy (kWh) × Tariff Rate

Example:
---------
Energy = 5.2 kWh
Tariff = ₹8.50 / kWh

Cost = 5.2 × 8.50
     = ₹44.20

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from typing import Dict, List, Tuple

from simulator.core.config import (
    ELECTRICITY_RATE_PER_KWH,
    CURRENCY_SYMBOL
)


class CostCalculator:
    """
    Tracks cumulative electricity costs.
    """

    def __init__(
        self,
        tariff_rate: float = ELECTRICITY_RATE_PER_KWH
    ):
        """
        Initialize calculator.

        Parameters
        ----------
        tariff_rate : float
            Electricity cost per kWh.
        """

        self.tariff_rate = tariff_rate
        self.total_cost = 0.0

    def calculate_cost(
        self,
        energy_kwh: float
    ) -> float:
        """
        Calculate cost using flat-rate billing.

        Parameters
        ----------
        energy_kwh : float

        Returns
        -------
        float
            Estimated cost.
        """

        return round(
            energy_kwh * self.tariff_rate,
            2
        )

    def add_consumption(
        self,
        energy_kwh: float
    ) -> Dict[str, float]:
        """
        Add energy consumption and update
        cumulative billing totals.

        Parameters
        ----------
        energy_kwh : float

        Returns
        -------
        dict
        """

        interval_cost = self.calculate_cost(
            energy_kwh
        )

        self.total_cost += interval_cost

        return {
            "interval_cost": round(
                interval_cost,
                2
            ),
            "total_cost": round(
                self.total_cost,
                2
            )
        }

    def get_total_cost(self) -> float:
        """
        Return cumulative cost.
        """

        return round(
            self.total_cost,
            2
        )

    def reset(self):
        """
        Reset cost tracking.
        """

        self.total_cost = 0.0

    def get_summary(self) -> Dict[str, float]:
        """
        Return billing summary.
        """

        return {
            "tariff_rate": self.tariff_rate,
            "currency": CURRENCY_SYMBOL,
            "total_cost": round(
                self.total_cost,
                2
            )
        }


# ==========================================================
# TIERED TARIFF CALCULATOR
# ==========================================================

class TieredCostCalculator:
    """
    Tiered/slab-based billing calculator.

    Example Slabs:

    0–100 kWh   -> ₹6.00
    101–300 kWh -> ₹8.00
    301+ kWh    -> ₹10.00
    """

    def __init__(
        self,
        slabs: List[Tuple[float, float]]
    ):
        """
        Parameters
        ----------
        slabs : list

        Example:
        [
            (100, 6),
            (300, 8),
            (float("inf"), 10)
        ]
        """

        self.slabs = slabs

    def calculate_cost(
        self,
        energy_kwh: float
    ) -> float:
        """
        Calculate slab-based electricity bill.
        """

        remaining = energy_kwh
        previous_limit = 0
        total_cost = 0.0

        for limit, rate in self.slabs:

            slab_units = min(
                remaining,
                limit - previous_limit
            )

            if slab_units <= 0:
                break

            total_cost += (
                slab_units * rate
            )

            remaining -= slab_units
            previous_limit = limit

        return round(
            total_cost,
            2
        )


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def calculate_cost(
    energy_kwh: float,
    tariff_rate: float = ELECTRICITY_RATE_PER_KWH
) -> float:
    """
    Quick flat-rate cost calculation.
    """

    return round(
        energy_kwh * tariff_rate,
        2
    )


def estimate_daily_cost(
    daily_energy_kwh: float
) -> float:
    """
    Estimate daily electricity cost.
    """

    return calculate_cost(
        daily_energy_kwh
    )


def estimate_monthly_cost(
    monthly_energy_kwh: float
) -> float:
    """
    Estimate monthly electricity cost.
    """

    return calculate_cost(
        monthly_energy_kwh
    )


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    print("\nFlat Rate Billing\n")

    calculator = CostCalculator()

    result = calculator.add_consumption(
        energy_kwh=5.75
    )

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nSummary\n")
    print(calculator.get_summary())

    print("\nTiered Billing Example\n")

    slab_calculator = TieredCostCalculator(
        slabs=[
            (100, 6),
            (300, 8),
            (float("inf"), 10)
        ]
    )

    bill = slab_calculator.calculate_cost(
        energy_kwh=350
    )

    print(
        f"350 kWh Bill: "
        f"{CURRENCY_SYMBOL}{bill}"
    )