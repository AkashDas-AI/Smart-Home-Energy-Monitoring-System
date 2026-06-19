"""
Smart Home Energy Monitoring System - Reporting Package.

This package contains all reporting and export-related modules used by
the Smart Home Energy Monitoring System.

The reporting layer is responsible for transforming raw telemetry and
analytical outputs into structured files that can be stored, reviewed,
shared, and visualized.

Core Responsibilities:
- CSV telemetry export
- Historical data archival
- Daily energy reports
- Monthly energy reports
- PDF report generation
- Cost and consumption summaries
- Alert event logging
- Sample dataset generation

Modules:
- csv_exporter.py
    Handles structured export of time-series energy telemetry,
    appliance statistics, alerts, and consumption records.

- pdf_exporter.py
    Generates professional PDF reports containing energy usage,
    billing summaries, alert history, and system statistics.

- alert_logger.py
    Stores alert events in CSV format for later analysis,
    troubleshooting, and audit purposes.

- sample_data_generator.py
    Creates lightweight sample datasets from generated telemetry
    logs for demonstrations, testing, documentation, and GitHub
    portfolio presentation.

Generated Outputs:
- CSV Logs
- Daily Reports
- Monthly Reports
- Energy Consumption Summaries
- Cost Analysis Reports
- Alert Reports
- Alert Event Logs
- Sample Datasets

Design Goals:
- Clean separation from simulation logic
- Reusable export interfaces
- Dashboard-independent reporting
- Human-readable report formats
- Easy integration with future analytics modules

Typical Workflow:
Telemetry Data
       ↓
Analytics Engine
       ↓
Reporting Package
       ↓
CSV Export
       ↓
PDF Report Generation
       ↓
Archive / Share / Review

This package intentionally focuses on reporting concerns only and does
not perform simulation, MQTT communication, or power calculations.

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

__all__ = [
    "csv_exporter",
    "pdf_exporter",
    "alert_logger",
    "sample_data_generator"
]