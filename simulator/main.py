"""
Smart Home Energy Monitoring System - Main Simulator Engine.

This module serves as the central execution driver for the entire
Smart Home Energy Monitoring System simulation environment.

Responsibilities:
-----------------
1. Generate simulated electrical telemetry
2. Calculate power metrics
3. Calculate accumulated energy usage
4. Estimate electricity costs
5. Evaluate alert conditions
6. Export telemetry to CSV
7. Publish telemetry via MQTT
8. Generate periodic reports

Execution Flow:
---------------
Energy Simulator
        ↓
Power Analytics
        ↓
Energy Analytics
        ↓
Cost Estimation
        ↓
Alert Evaluation
        ↓
CSV Export
        ↓
MQTT Publishing
        ↓
Dashboard / Monitoring

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from datetime import datetime
import time

from dashboard.thingspeak.thingspeak_client import ThingSpeakClient
from simulator.core.config import (
    SIMULATION_INTERVAL_SECONDS,
    ENABLE_ALERTS,
    ENABLE_CSV_LOGGING,
    ENABLE_PDF_REPORTS
)

from simulator.core.energy_simulator import (
    EnergySimulator
)

from simulator.core.alert_engine import (
    AlertEngine
)

from simulator.analytics.energy_calculator import (
    EnergyCalculator
)

from simulator.analytics.cost_calculator import (
    CostCalculator
)

from simulator.reports.csv_exporter import (
    CSVExporter
)

from simulator.reports.pdf_exporter import (
    PDFExporter
)

from simulator.reports.alert_logger import (
    AlertLogger
)

from simulator.reports.sample_data_generator import (
    SampleDataGenerator
)

from simulator.communication.mqtt_publisher import (
    MQTTPublisher
)

from dashboard.thingspeak import (
    ThingSpeakClient
)


# ==========================================================
# MAIN APPLICATION
# ==========================================================

class SmartHomeEnergyMonitor:
    """
    Main simulator controller.
    """

    def __init__(self):
        """
        Initialize all project components.
        """

        self.simulator = EnergySimulator()

        self.energy_calculator = (
            EnergyCalculator()
        )

        self.cost_calculator = (
            CostCalculator()
        )

        self.alert_engine = (
            AlertEngine()
        )

        self.csv_exporter = (
            CSVExporter()
        )

        self.pdf_exporter = (
            PDFExporter()
        )

        self.alert_logger = (
            AlertLogger()
        )

        self.sample_data_generator = (
            SampleDataGenerator()
        )

        self.mqtt_publisher = (
            MQTTPublisher()
        )

        # ThingSpeak client
        self.thingspeak_client = (
            ThingSpeakClient()
        )

        # Publish to ThingSpeak every
        # 15 simulation cycles
        self.thingspeak_counter = 0

        self.running = False

    # ======================================================
    # STARTUP
    # ======================================================

    def initialize(self):
        """
        Initialize system resources.
        """

        print("\n" + "=" * 60)
        print("SMART HOME ENERGY MONITORING SYSTEM")
        print("=" * 60)

        print("\nInitializing Components...")

        mqtt_connected = (
            self.mqtt_publisher.connect()
        )

        if mqtt_connected:
            print(
                "[OK] MQTT Connected"
            )
        else:
            print(
                "[WARNING] MQTT Not Available"
            )

        self.running = True

        print(
            "[OK] System Ready\n"
        )

    # ======================================================
    # TELEMETRY PIPELINE
    # ======================================================

    def process_cycle(self):
        """
        Execute one monitoring cycle.
        """

        # ----------------------------------------------
        # Generate telemetry
        # ----------------------------------------------

        telemetry = (
            self.simulator
            .generate_measurement()
        )

        active_power = (
            telemetry["active_power_w"]
        )

        power_factor = (
            telemetry["power_factor"]
        )

        voltage = (
            telemetry["voltage"]
        )

        current = (
            telemetry["current"]
        )

        # ----------------------------------------------
        # Energy Calculation
        # ----------------------------------------------

        energy_stats = (
            self.energy_calculator
            .add_consumption(
                power_watts=active_power,
                duration_seconds=
                SIMULATION_INTERVAL_SECONDS
            )
        )

        total_energy_kwh = (
            energy_stats[
                "total_energy_kwh"
            ]
        )

        # ----------------------------------------------
        # Cost Calculation
        # ----------------------------------------------

        cost_stats = (
            self.cost_calculator
            .add_consumption(
                energy_kwh=
                energy_stats[
                    "interval_energy_kwh"
                ]
            )
        )

        total_cost = (
            cost_stats["total_cost"]
        )

        # ----------------------------------------------
        # Alert Processing
        # ----------------------------------------------

        alerts = []

        if ENABLE_ALERTS:

            alerts = (
                self.alert_engine
                .evaluate(
                    voltage=voltage,
                    current=current,
                    power_watts=
                    active_power,
                    energy_kwh=
                    total_energy_kwh,
                    power_factor=
                    power_factor
                )
            )

        alert_status = (
            "ALERT"
            if alerts
            else "NORMAL"
        )

        # ----------------------------------------------
        # Final Payload
        # ----------------------------------------------

        payload = {
            **telemetry,

            "energy_kwh":
                total_energy_kwh,

            "estimated_cost":
                total_cost,

            "alert_status":
                alert_status,

            "alert_count":
                len(alerts)
        }

        # ----------------------------------------------
        # Alert Logging
        # ----------------------------------------------

        if alerts:

            for alert in alerts:

                self.alert_logger.log_alert(
                    appliance=payload["appliance"],
                    power_w=payload["active_power_w"],
                    energy_kwh=payload["energy_kwh"],
                    alert_count=payload["alert_count"],
                    status=payload["alert_status"]
                )   

        # ----------------------------------------------
        # CSV Export
        # ----------------------------------------------

        if ENABLE_CSV_LOGGING:

            self.csv_exporter.append_record(
                payload
            )

        # ----------------------------------------------
        # MQTT Publish
        # ----------------------------------------------

        self.mqtt_publisher.publish_telemetry(
            payload
        )

        for alert in alerts:

            self.mqtt_publisher.publish_alert(
                alert
            )

        # ----------------------------------------------
        # ThingSpeak Publish
        # ----------------------------------------------

        self.thingspeak_counter += 1

        if self.thingspeak_counter >= 15:

            try:

                self.thingspeak_client.publish_energy_data(
                    voltage=voltage,
                    current=current,
                    power=active_power,
                    energy_kwh=total_energy_kwh,
                    cost=total_cost,
                    power_factor=power_factor,
                    alert_count=len(alerts),
                    status=1
                )

            except Exception as exc:

                print(
                    f"[ThingSpeak Error] {exc}"
             )

            finally:

                self.thingspeak_counter = 0    

        # ----------------------------------------------
        # Console Output
        # ----------------------------------------------

        self.display_payload(
            payload
        )

        return payload

    # ======================================================
    # DISPLAY
    # ======================================================

    @staticmethod
    def display_payload(
        payload
    ):
        """
        Display telemetry.
        """

        print(
            f"[{datetime.now().strftime('%H:%M:%S')}] "
            f"{payload['appliance']} | "
            f"{payload['active_power_w']} W | "
            f"{payload['energy_kwh']:.6f} kWh | "
            f"₹{payload['estimated_cost']:.2f} | "
            f"{payload['alert_status']}"
        )

    # ======================================================
    # REPORTS
    # ======================================================

    def generate_summary_report(self):
        """
        Generate end-of-session PDF report.
        """

        if not ENABLE_PDF_REPORTS:
            return

        total_energy = (
            self.energy_calculator
            .get_total_energy_kwh()
        )

        total_cost = (
            self.cost_calculator
            .get_total_cost()
        )

        report_path = (
            self.pdf_exporter
            .generate_daily_report(
                energy_kwh=
                total_energy,

                cost=
                total_cost,

                average_power=0,

                alert_count=0
            )
        )

        print(
            "\nPDF Report Generated:"
        )

        print(report_path)

    # ======================================================
    # RUN LOOP
    # ======================================================

    def run(
        self,
        cycles: int = None
    ):
        """
        Start simulator.

        Parameters
        ----------
        cycles : int, optional

        None = infinite run
        """

        self.initialize()

        try:

            if cycles is None:

                while self.running:

                    self.process_cycle()

                    time.sleep(
                        SIMULATION_INTERVAL_SECONDS
                    )

            else:

                for _ in range(cycles):

                    self.process_cycle()

                    time.sleep(
                        SIMULATION_INTERVAL_SECONDS
                    )

        except KeyboardInterrupt:

            print(
                "\n\nStopping Simulator..."
            )

        finally:

            self.shutdown()

    # ======================================================
    # SHUTDOWN
    # ======================================================

    def shutdown(self):
        """
        Gracefully stop system.
        """

        self.running = False

        self.generate_summary_report()

        self.sample_data_generator.generate(
            max_rows=100
            )

        self.mqtt_publisher.publish_status(
            "OFFLINE"
        )

        self.mqtt_publisher.disconnect()

        print(
            "\nSystem Shutdown Complete."
        )


# ==========================================================
# ENTRY POINT
# ==========================================================

def main():
    """
    Application entry point.
    """

    monitor = (
        SmartHomeEnergyMonitor()
    )

    # Change to None for continuous mode
    monitor.run(cycles=100)


if __name__ == "__main__":
    main()