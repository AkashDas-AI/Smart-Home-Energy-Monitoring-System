"""
Smart Home Energy Monitoring System - CSV Exporter.

This module provides utilities for exporting simulator telemetry,
energy analytics, cost estimates, and alert information into
structured CSV files.

The exporter is designed to:

- Automatically create CSV files if they do not exist
- Append new telemetry records efficiently
- Preserve column consistency
- Support long-term logging and analysis
- Enable future dashboard and reporting integrations

Typical Exported Data:
----------------------
- Timestamp
- Voltage
- Current
- Active Power
- Apparent Power
- Reactive Power
- Energy Consumption
- Cost Estimates
- Power Factor
- Alert Status

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List
import csv

from simulator.core.config import (
    CSV_LOGS_DIR,
    CSV_FILENAME
)


class CSVExporter:
    """
    Handles CSV logging and export operations.
    """

    def __init__(
        self,
        output_directory: Path = CSV_LOGS_DIR,
        filename: str = CSV_FILENAME
    ):
        """
        Initialize exporter.
        """

        self.output_directory = Path(output_directory)

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.file_path = (
            self.output_directory / filename
        )

    def file_exists(self) -> bool:
        """
        Check whether CSV file exists.
        """

        return self.file_path.exists()

    def write_header(
        self,
        fieldnames: List[str]
    ) -> None:
        """
        Create CSV file and write header row.
        """

        with open(
            self.file_path,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames
            )

            writer.writeheader()

    def append_record(
        self,
        record: Dict
    ) -> None:
        """
        Append a telemetry record.

        Parameters
        ----------
        record : dict
        """

        fieldnames = list(record.keys())

        if not self.file_exists():
            self.write_header(
                fieldnames
            )

        with open(
            self.file_path,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames
            )

            writer.writerow(record)

    def append_records(
        self,
        records: List[Dict]
    ) -> None:
        """
        Append multiple records.
        """

        if not records:
            return

        fieldnames = list(
            records[0].keys()
        )

        if not self.file_exists():
            self.write_header(
                fieldnames
            )

        with open(
            self.file_path,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames
            )

            writer.writerows(records)

    def get_file_path(self) -> Path:
        """
        Return CSV file path.
        """

        return self.file_path

    def export_alert(
        self,
        alert_data: Dict
    ) -> None:
        """
        Export alert record.

        Creates or appends to alerts.csv.
        """

        alert_file = (
            self.output_directory /
            "alerts.csv"
        )

        fieldnames = list(
            alert_data.keys()
        )

        file_exists = alert_file.exists()

        with open(
            alert_file,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=fieldnames
            )

            if not file_exists:
                writer.writeheader()

            writer.writerow(alert_data)

    def create_daily_snapshot(
        self,
        summary_data: Dict
    ) -> Path:
        """
        Export daily summary snapshot.
        """

        timestamp = datetime.now().strftime(
            "%Y-%m-%d"
        )

        snapshot_file = (
            self.output_directory /
            f"daily_summary_{timestamp}.csv"
        )

        with open(
            snapshot_file,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as csv_file:

            writer = csv.DictWriter(
                csv_file,
                fieldnames=list(
                    summary_data.keys()
                )
            )

            writer.writeheader()
            writer.writerow(summary_data)

        return snapshot_file


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def export_record(
    record: Dict
) -> None:
    """
    Quick export helper.
    """

    exporter = CSVExporter()

    exporter.append_record(
        record
    )


def export_records(
    records: List[Dict]
) -> None:
    """
    Quick bulk export helper.
    """

    exporter = CSVExporter()

    exporter.append_records(
        records
    )


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    exporter = CSVExporter()

    sample_record = {
        "timestamp":
            datetime.now().isoformat(),
        "voltage":
            229.8,
        "current":
            3.42,
        "active_power_w":
            710.5,
        "energy_kwh":
            1.28,
        "cost":
            10.88,
        "power_factor":
            0.91,
        "alert_status":
            "NORMAL"
    }

    exporter.append_record(
        sample_record
    )

    print(
        "\nTelemetry exported successfully."
    )

    print(
        f"\nCSV File: "
        f"{exporter.get_file_path()}"
    )