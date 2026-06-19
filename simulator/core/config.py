"""
Smart Home Energy Monitoring System - Configuration Module.

This module centralizes all configurable parameters used throughout the
simulation environment.

The goal is to ensure that operational values such as electrical limits,
tariff rates, MQTT settings, reporting paths, and simulator behavior are
managed from a single source of truth.

Benefits:
- Easier maintenance
- Cleaner imports
- Environment-specific customization
- Reduced hardcoded values
- Better scalability

Author: Akash Das
Project: Smart Home Energy Monitoring System
"""

from pathlib import Path
import os

# ==========================================================
# PROJECT ROOT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
SAMPLE_DATA_DIR = DATA_DIR / "sample_data"

REPORTS_DIR = PROJECT_ROOT / "reports"
DAILY_REPORTS_DIR = REPORTS_DIR / "daily"
MONTHLY_REPORTS_DIR = REPORTS_DIR / "monthly"
PDF_REPORTS_DIR = REPORTS_DIR / "pdf"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
CSV_LOGS_DIR = OUTPUTS_DIR / "csv_logs"
ALERTS_DIR = OUTPUTS_DIR / "alerts"
EXPORTS_DIR = OUTPUTS_DIR / "exports"

# ==========================================================
# ELECTRICAL SYSTEM CONFIGURATION
# ==========================================================

# Nominal single-phase household voltage (India)
NOMINAL_VOLTAGE = 230.0  # Volts

# Acceptable operating range
MIN_VOLTAGE = 210.0
MAX_VOLTAGE = 250.0

# Frequency (India)
GRID_FREQUENCY = 50.0  # Hz

# ==========================================================
# CURRENT THRESHOLDS
# ==========================================================

MAX_CURRENT = 15.0      # Amps
WARNING_CURRENT = 10.0  # Amps

# ==========================================================
# POWER THRESHOLDS
# ==========================================================

MAX_POWER = 3000.0      # Watts
WARNING_POWER = 2000.0  # Watts

# ==========================================================
# ENERGY THRESHOLDS
# ==========================================================

DAILY_ENERGY_LIMIT_KWH = 15.0
MONTHLY_ENERGY_LIMIT_KWH = 450.0

# ==========================================================
# ELECTRICITY TARIFF
# ==========================================================

# Flat-rate tariff
ELECTRICITY_RATE_PER_KWH = float(
    os.getenv("ELECTRICITY_RATE", 8.50)
)

# Currency display
CURRENCY_SYMBOL = "₹"

# ==========================================================
# MQTT CONFIGURATION
# ==========================================================

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")

MQTT_PORT = int(
    os.getenv("MQTT_PORT", 1883)
)

MQTT_KEEPALIVE = 60

MQTT_TOPIC = os.getenv(
    "MQTT_TOPIC",
    "home/energy/node1"
)

MQTT_CLIENT_ID = "smart-home-energy-simulator"

# ==========================================================
# SIMULATOR SETTINGS
# ==========================================================

SIMULATION_INTERVAL_SECONDS = int(
    os.getenv("SIMULATION_INTERVAL", 1)
)

ENABLE_RANDOM_NOISE = True

NOISE_PERCENTAGE = 0.05
# ±5% variation

# ==========================================================
# ALERT SETTINGS
# ==========================================================

ENABLE_ALERTS = True

OVERCURRENT_THRESHOLD = 12.0
OVERVOLTAGE_THRESHOLD = 245.0
OVERVOLTAGE_WARNING = 240.0

OVERLOAD_POWER_THRESHOLD = 2500.0

# ==========================================================
# REPORTING SETTINGS
# ==========================================================

ENABLE_CSV_LOGGING = True
ENABLE_PDF_REPORTS = True

CSV_FILENAME = "energy_log.csv"

# ==========================================================
# DASHBOARD SETTINGS
# ==========================================================

ENABLE_DASHBOARD_UPDATES = True

# ==========================================================
# LOGGING SETTINGS
# ==========================================================

LOG_LEVEL = "INFO"

# ==========================================================
# PAYLOAD SETTINGS
# ==========================================================

DEVICE_ID = "SIM_NODE_001"

LOCATION = "Virtual Smart Home"

# ==========================================================
# MQTT PAYLOAD KEYS
# ==========================================================

PAYLOAD_KEYS = [
    "timestamp",
    "voltage",
    "current",
    "power",
    "apparent_power",
    "reactive_power",
    "energy_kwh",
    "cost",
    "power_factor",
    "alert_status",
]

# ==========================================================
# STARTUP VALIDATION
# ==========================================================

REQUIRED_DIRECTORIES = [
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    SAMPLE_DATA_DIR,
    DAILY_REPORTS_DIR,
    MONTHLY_REPORTS_DIR,
    PDF_REPORTS_DIR,
    CSV_LOGS_DIR,
    ALERTS_DIR,
    EXPORTS_DIR,
]

for directory in REQUIRED_DIRECTORIES:
    directory.mkdir(parents=True, exist_ok=True)

# ==========================================================
# CONFIGURATION SUMMARY
# ==========================================================

CONFIG_SUMMARY = {
    "voltage": NOMINAL_VOLTAGE,
    "frequency": GRID_FREQUENCY,
    "tariff": ELECTRICITY_RATE_PER_KWH,
    "mqtt_broker": MQTT_BROKER,
    "mqtt_port": MQTT_PORT,
    "simulation_interval": SIMULATION_INTERVAL_SECONDS,
}