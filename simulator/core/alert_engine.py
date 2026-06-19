"""
Smart Home Energy Monitoring System - Alert Engine.

This module is responsible for evaluating incoming electrical telemetry
and detecting abnormal operating conditions.

The alert engine acts as a simplified version of the rule-based monitoring
systems commonly used in:

- Smart Homes
- Building Energy Management Systems (BEMS)
- Industrial Monitoring Systems
- Energy Analytics Platforms
- Smart Grid Infrastructure

Detected Conditions:
--------------------
- Overvoltage
- Undervoltage
- Overcurrent
- Power Overload
- Excessive Energy Consumption
- Abnormal Power Factor

Each detected condition generates a structured alert object that can be:

- Displayed on dashboards
- Logged to files
- Published via MQTT
- Trigger a buzzer/relay on ESP32 hardware

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from datetime import datetime
from typing import Dict, List

from simulator.core.config import (
    MIN_VOLTAGE,
    MAX_VOLTAGE,
    WARNING_CURRENT,
    MAX_CURRENT,
    WARNING_POWER,
    MAX_POWER,
    DAILY_ENERGY_LIMIT_KWH
)


# ==========================================================
# ALERT SEVERITY LEVELS
# ==========================================================

INFO = "INFO"
WARNING = "WARNING"
CRITICAL = "CRITICAL"


# ==========================================================
# ALERT ENGINE
# ==========================================================

class AlertEngine:
    """
    Rule-based electrical anomaly detector.
    """

    def __init__(self):
        self.active_alerts = []

    @staticmethod
    def _build_alert(
        alert_type: str,
        severity: str,
        message: str,
        value: float
    ) -> Dict:
        """
        Create a standardized alert object.
        """

        return {
            "timestamp": datetime.now().isoformat(),
            "alert_type": alert_type,
            "severity": severity,
            "message": message,
            "value": value
        }

    def check_voltage(
        self,
        voltage: float
    ) -> List[Dict]:
        """
        Check voltage conditions.
        """

        alerts = []

        if voltage > MAX_VOLTAGE:
            alerts.append(
                self._build_alert(
                    alert_type="OVERVOLTAGE",
                    severity=CRITICAL,
                    message=(
                        f"Voltage exceeded "
                        f"maximum limit "
                        f"({MAX_VOLTAGE}V)"
                    ),
                    value=voltage
                )
            )

        elif voltage < MIN_VOLTAGE:
            alerts.append(
                self._build_alert(
                    alert_type="UNDERVOLTAGE",
                    severity=CRITICAL,
                    message=(
                        f"Voltage below "
                        f"minimum limit "
                        f"({MIN_VOLTAGE}V)"
                    ),
                    value=voltage
                )
            )

        return alerts

    def check_current(
        self,
        current: float
    ) -> List[Dict]:
        """
        Check current conditions.
        """

        alerts = []

        if current >= MAX_CURRENT:

            alerts.append(
                self._build_alert(
                    alert_type="OVERCURRENT",
                    severity=CRITICAL,
                    message=(
                        f"Current exceeded "
                        f"maximum threshold "
                        f"({MAX_CURRENT}A)"
                    ),
                    value=current
                )
            )

        elif current >= WARNING_CURRENT:

            alerts.append(
                self._build_alert(
                    alert_type="HIGH_CURRENT",
                    severity=WARNING,
                    message=(
                        f"Current approaching "
                        f"critical threshold "
                        f"({WARNING_CURRENT}A)"
                    ),
                    value=current
                )
            )

        return alerts

    def check_power(
        self,
        power_watts: float
    ) -> List[Dict]:
        """
        Check power consumption.
        """

        alerts = []

        if power_watts >= MAX_POWER:

            alerts.append(
                self._build_alert(
                    alert_type="POWER_OVERLOAD",
                    severity=CRITICAL,
                    message=(
                        f"Power exceeded "
                        f"maximum threshold "
                        f"({MAX_POWER}W)"
                    ),
                    value=power_watts
                )
            )

        elif power_watts >= WARNING_POWER:

            alerts.append(
                self._build_alert(
                    alert_type="HIGH_POWER_USAGE",
                    severity=WARNING,
                    message=(
                        f"Power consumption "
                        f"is unusually high"
                    ),
                    value=power_watts
                )
            )

        return alerts

    def check_energy_usage(
        self,
        energy_kwh: float
    ) -> List[Dict]:
        """
        Check accumulated energy usage.
        """

        alerts = []

        if energy_kwh >= DAILY_ENERGY_LIMIT_KWH:

            alerts.append(
                self._build_alert(
                    alert_type="HIGH_ENERGY_USAGE",
                    severity=WARNING,
                    message=(
                        f"Daily energy usage "
                        f"limit exceeded "
                        f"({DAILY_ENERGY_LIMIT_KWH} kWh)"
                    ),
                    value=energy_kwh
                )
            )

        return alerts

    def check_power_factor(
        self,
        power_factor: float
    ) -> List[Dict]:
        """
        Check power factor quality.
        """

        alerts = []

        if power_factor < 0.70:

            alerts.append(
                self._build_alert(
                    alert_type="LOW_POWER_FACTOR",
                    severity=WARNING,
                    message=(
                        "Poor power factor "
                        "detected"
                    ),
                    value=power_factor
                )
            )

        return alerts

    def evaluate(
        self,
        voltage: float,
        current: float,
        power_watts: float,
        energy_kwh: float,
        power_factor: float
    ) -> List[Dict]:
        """
        Perform complete system evaluation.

        Returns all triggered alerts.
        """

        alerts = []

        alerts.extend(
            self.check_voltage(voltage)
        )

        alerts.extend(
            self.check_current(current)
        )

        alerts.extend(
            self.check_power(power_watts)
        )

        alerts.extend(
            self.check_energy_usage(
                energy_kwh
            )
        )

        alerts.extend(
            self.check_power_factor(
                power_factor
            )
        )

        self.active_alerts = alerts

        return alerts

    def has_alerts(self) -> bool:
        """
        Check whether alerts exist.
        """

        return len(self.active_alerts) > 0

    def get_highest_severity(self) -> str:
        """
        Return highest alert severity.
        """

        if not self.active_alerts:
            return INFO

        severities = [
            alert["severity"]
            for alert in self.active_alerts
        ]

        if CRITICAL in severities:
            return CRITICAL

        if WARNING in severities:
            return WARNING

        return INFO

    def get_alert_summary(self) -> Dict:
        """
        Return dashboard-friendly summary.
        """

        return {
            "alert_count": len(
                self.active_alerts
            ),
            "highest_severity":
                self.get_highest_severity(),
            "alerts":
                self.active_alerts
        }


# ==========================================================
# CONVENIENCE FUNCTION
# ==========================================================

def evaluate_alerts(
    voltage: float,
    current: float,
    power_watts: float,
    energy_kwh: float,
    power_factor: float
) -> List[Dict]:
    """
    Quick evaluation helper.
    """

    engine = AlertEngine()

    return engine.evaluate(
        voltage=voltage,
        current=current,
        power_watts=power_watts,
        energy_kwh=energy_kwh,
        power_factor=power_factor
    )


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    engine = AlertEngine()

    alerts = engine.evaluate(
        voltage=255,
        current=12.5,
        power_watts=2800,
        energy_kwh=18,
        power_factor=0.65
    )

    print("\nAlert Results\n")

    for alert in alerts:
        print(alert)

    print("\nSummary\n")
    print(engine.get_alert_summary())