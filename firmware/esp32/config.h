/*
==========================================================
Smart Home Energy Monitoring System
ESP32 Configuration File
==========================================================

Purpose:
Centralized configuration settings for the ESP32-based
energy monitoring node.

Contains:

- Wi-Fi credentials
- MQTT broker settings
- Device identification
- GPIO assignments
- Sensor calibration constants
- Alert thresholds
- Sampling configuration

Author: Akash Das
==========================================================
*/

#ifndef CONFIG_H
#define CONFIG_H

// ==========================================================
// DEVICE INFORMATION
// ==========================================================

#define DEVICE_ID          "ESP32_NODE_001"
#define DEVICE_LOCATION    "Smart Home Lab"

// ==========================================================
// WIFI CONFIGURATION
// ==========================================================

#define WIFI_SSID          "YOUR_WIFI_NAME"
#define WIFI_PASSWORD      "YOUR_WIFI_PASSWORD"

// ==========================================================
// MQTT CONFIGURATION
// ==========================================================

#define MQTT_BROKER        "192.168.1.100"
#define MQTT_PORT          1883

#define MQTT_TELEMETRY_TOPIC \
"home/energy/node1/telemetry"

#define MQTT_ALERT_TOPIC \
"home/energy/node1/alerts"

#define MQTT_STATUS_TOPIC \
"home/energy/node1/status"

// ==========================================================
// GPIO PIN ASSIGNMENTS
// ==========================================================

// ACS712 Current Sensor

#define CURRENT_SENSOR_PIN     34

// Voltage Sensor

#define VOLTAGE_SENSOR_PIN     35

// Relay Module

#define RELAY_PIN              26

// LEDs

#define GREEN_LED_PIN          18
#define YELLOW_LED_PIN         19
#define RED_LED_PIN            21

// Buzzer

#define BUZZER_PIN             23

// ==========================================================
// ADC CONFIGURATION
// ==========================================================

#define ADC_RESOLUTION         4095.0f
#define ADC_REFERENCE_VOLTAGE  3.3f

// ==========================================================
// ACS712 CURRENT SENSOR
// ==========================================================

// ACS712-20A Version

#define ACS712_SENSITIVITY     0.100f
#define ACS712_ZERO_CURRENT    2.50f

// ==========================================================
// VOLTAGE SENSOR CALIBRATION
// ==========================================================

// ZMPT101B or equivalent module

#define VOLTAGE_CALIBRATION_FACTOR  100.0f

// ==========================================================
// ELECTRICAL PARAMETERS
// ==========================================================

#define NOMINAL_VOLTAGE        230.0f
#define NOMINAL_FREQUENCY      50.0f

// Default residential load power factor

#define DEFAULT_POWER_FACTOR   0.90f

// ==========================================================
// ALERT THRESHOLDS
// ==========================================================

// Voltage Limits

#define MIN_VOLTAGE_THRESHOLD  200.0f
#define MAX_VOLTAGE_THRESHOLD  250.0f

// Current Limits

#define WARNING_CURRENT        10.0f
#define MAX_CURRENT            15.0f

// Power Limits

#define WARNING_POWER          2000.0f
#define MAX_POWER              3000.0f

// Daily Consumption Limit

#define DAILY_ENERGY_LIMIT     15.0f

// ==========================================================
// SAMPLING CONFIGURATION
// ==========================================================

#define SENSOR_SAMPLE_COUNT    100

#define TELEMETRY_INTERVAL_MS  1000

#define ALERT_CHECK_INTERVAL   1000

// ==========================================================
// BUZZER CONFIGURATION
// ==========================================================

#define BUZZER_FREQUENCY       2000
#define BUZZER_DURATION_MS     500

// ==========================================================
// RELAY CONFIGURATION
// ==========================================================

#define RELAY_ACTIVE_HIGH      true

// ==========================================================
// JSON BUFFER SIZES
// ==========================================================

#define MQTT_JSON_BUFFER_SIZE  512

// ==========================================================
// SERIAL DEBUG
// ==========================================================

#define SERIAL_BAUD_RATE       115200

#define DEBUG_MODE             true

#endif

/*
==========================================================
END OF FILE
==========================================================
*/