"""
Smart Home Energy Monitoring System - Sample Data Generator.

This module automatically generates a lightweight sample dataset
from the primary telemetry log file.

Purpose:
--------
- Portfolio demonstrations
- GitHub repository examples
- Testing and validation
- Documentation screenshots

Source:
-------
outputs/csv_logs/energy_log.csv

Output:
-------
data/sample_data/sample_energy_data.csv

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

import csv

from simulator.core.config import (
    CSV_LOGS_DIR,
    SAMPLE_DATA_DIR
)


class SampleDataGenerator:
    """
    Generate sample datasets from existing telemetry logs.
    """

    def __init__(self):
        """
        Initialize source and destination files.
        """

        self.source_file = (
            CSV_LOGS_DIR /
            "energy_log.csv"
        )

        self.destination_file = (
            SAMPLE_DATA_DIR /
            "sample_energy_data.csv"
        )

    # ======================================================
    # SAMPLE DATA GENERATION
    # ======================================================

    def generate(
        self,
        max_rows: int = 50
    ):
        """
        Generate a lightweight sample dataset.

        Parameters
        ----------
        max_rows : int
            Maximum number of telemetry rows
            to include in the sample file.

        Returns
        -------
        bool
            True if successful.
        """

        if not self.source_file.exists():
            return False

        with open(
            self.source_file,
            mode="r",
            encoding="utf-8"
        ) as source:

            reader = csv.reader(source)
            rows = list(reader)

        if not rows:
            return False

        # Preserve header row
        rows_to_save = rows[:max_rows + 1]

        with open(
            self.destination_file,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as destination:

            writer = csv.writer(destination)
            writer.writerows(rows_to_save)

        return True