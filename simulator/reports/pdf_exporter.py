"""
Smart Home Energy Monitoring System - PDF Exporter.

This module generates professional PDF reports containing
energy consumption statistics, electricity cost summaries,
electrical metrics, and alert information.

The generated reports are designed to resemble simplified
energy reports used by:

- Smart Home Platforms
- Utility Providers
- Building Energy Management Systems
- Energy Auditing Services
- IoT Monitoring Dashboards

Generated Reports:
------------------
- Daily Energy Report
- Monthly Energy Report
- Cost Summary Report
- Consumption Summary Report
- Alert Summary Report

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List

from fpdf import FPDF

from simulator.core.config import (
    PDF_REPORTS_DIR,
    CURRENCY_SYMBOL
)


# ==========================================================
# PDF EXPORTER
# ==========================================================

class PDFExporter:
    """
    Generates PDF energy reports.
    """

    def __init__(
        self,
        output_directory: Path = PDF_REPORTS_DIR
    ):
        """
        Initialize exporter.
        """

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def _create_pdf(self) -> FPDF:
        """
        Create configured PDF object.
        """

        pdf = FPDF()

        pdf.set_auto_page_break(
            auto=True,
            margin=15
        )

        pdf.add_page()

        return pdf

    def _add_title(
        self,
        pdf: FPDF,
        title: str
    ) -> None:
        """
        Add report title.
        """

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.cell(
            0,
            10,
            title,
            ln=True,
            align="C"
        )

        pdf.ln(5)

    def _add_timestamp(
        self,
        pdf: FPDF
    ) -> None:
        """
        Add generation timestamp.
        """

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        pdf.set_font(
            "Helvetica",
            size=10
        )

        pdf.cell(
            0,
            8,
            f"Generated: {timestamp}",
            ln=True
        )

        pdf.ln(4)

    def _add_section_header(
        self,
        pdf: FPDF,
        title: str
    ) -> None:
        """
        Add section heading.
        """

        pdf.set_font(
            "Helvetica",
            "B",
            14
        )

        pdf.cell(
            0,
            8,
            title,
            ln=True
        )

        pdf.ln(2)

    def _add_key_value_section(
        self,
        pdf: FPDF,
        data: Dict
    ) -> None:
        """
        Render dictionary contents.
        """

        pdf.set_font(
            "Helvetica",
            size=11
        )

        for key, value in data.items():

            label = (
                key.replace("_", " ")
                .title()
            )

            pdf.cell(
                0,
                7,
                f"{label}: {value}",
                ln=True
            )

        pdf.ln(4)

    def generate_energy_report(
        self,
        report_data: Dict,
        filename: str = None
    ) -> Path:
        """
        Generate a standard energy report.

        Parameters
        ----------
        report_data : dict

        filename : str, optional

        Returns
        -------
        Path
        """

        pdf = self._create_pdf()

        self._add_title(
            pdf,
            "Smart Home Energy Report"
        )

        self._add_timestamp(pdf)

        self._add_section_header(
            pdf,
            "Energy Consumption Summary"
        )

        self._add_key_value_section(
            pdf,
            report_data
        )

        if filename is None:

            filename = (
                f"energy_report_"
                f"{datetime.now():%Y%m%d_%H%M%S}.pdf"
            )

        file_path = (
            self.output_directory /
            filename
        )

        pdf.output(
            str(file_path)
        )

        return file_path

    def generate_daily_report(
        self,
        energy_kwh: float,
        cost: float,
        average_power: float,
        alert_count: int
    ) -> Path:
        """
        Generate daily summary report.
        """

        report_data = {
            "energy_kwh":
                round(energy_kwh, 4),

            "estimated_cost":
                f"INR {round(cost, 2)}",

            "average_power_w":
                round(average_power, 2),

            "alert_count":
                alert_count
        }

        return self.generate_energy_report(
            report_data,
            filename=(
                f"daily_report_"
                f"{datetime.now():%Y%m%d}.pdf"
            )
        )

    def generate_monthly_report(
        self,
        energy_kwh: float,
        cost: float,
        average_power: float,
        alert_count: int
    ) -> Path:
        """
        Generate monthly summary report.
        """

        report_data = {
            "energy_kwh":
                round(energy_kwh, 4),

            "estimated_cost":
                f"INR {round(cost, 2)}",

            "average_power_w":
                round(average_power, 2),

            "alert_count":
                alert_count
        }

        return self.generate_energy_report(
            report_data,
            filename=(
                f"monthly_report_"
                f"{datetime.now():%Y_%m}.pdf"
            )
        )

    def generate_alert_report(
        self,
        alerts: List[Dict]
    ) -> Path:
        """
        Generate alert report PDF.
        """

        pdf = self._create_pdf()

        self._add_title(
            pdf,
            "Alert Summary Report"
        )

        self._add_timestamp(pdf)

        self._add_section_header(
            pdf,
            "Detected Alerts"
        )

        if not alerts:

            pdf.set_font(
                "Helvetica",
                size=11
            )

            pdf.cell(
                0,
                8,
                "No alerts detected.",
                ln=True
            )

        else:

            pdf.set_font(
                "Helvetica",
                size=10
            )

            for alert in alerts:

                pdf.multi_cell(
                    0,
                    6,
                    (
                        f"[{alert.get('severity')}] "
                        f"{alert.get('alert_type')} - "
                        f"{alert.get('message')}"
                    )
                )

                pdf.ln(1)

        file_path = (
            self.output_directory /
            f"alert_report_"
            f"{datetime.now():%Y%m%d_%H%M%S}.pdf"
        )

        pdf.output(
            str(file_path)
        )

        return file_path


# ==========================================================
# CONVENIENCE FUNCTIONS
# ==========================================================

def create_energy_report(
    report_data: Dict
) -> Path:
    """
    Quick helper for generating
    a standard energy report.
    """

    exporter = PDFExporter()

    return exporter.generate_energy_report(
        report_data
    )


def create_daily_report(
    energy_kwh: float,
    cost: float,
    average_power: float,
    alert_count: int
) -> Path:
    """
    Quick helper for daily report.
    """

    exporter = PDFExporter()

    return exporter.generate_daily_report(
        energy_kwh=energy_kwh,
        cost=cost,
        average_power=average_power,
        alert_count=alert_count
    )


# ==========================================================
# MODULE TEST
# ==========================================================

if __name__ == "__main__":

    exporter = PDFExporter()

    report_file = (
        exporter.generate_daily_report(
            energy_kwh=12.45,
            cost=105.83,
            average_power=612.4,
            alert_count=2
        )
    )

    print(
        "\nPDF Report Generated Successfully"
    )

    print(
        f"\nFile Location:\n{report_file}"
    )