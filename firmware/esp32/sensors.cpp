/*
==========================================================
Smart Home Energy Monitoring System
sensors.cpp
==========================================================

Purpose:
Implementation of voltage and current sensor readings.

Supported Sensors:

1. ACS712 Current Sensor
2. Voltage Sensor Module (ZMPT101B compatible)

Author: Akash Das
==========================================================
*/

#include "sensors.h"
#include "config.h"

#include <math.h>

// ==========================================================
// GLOBAL INSTANCE
// ==========================================================

SensorManager Sensors;

// ==========================================================
// CONSTRUCTOR
// ==========================================================

SensorManager::SensorManager()
{
}

// ==========================================================
// INITIALIZATION
// ==========================================================

void SensorManager::begin()
{
    analogReadResolution(12);

    pinMode(CURRENT_SENSOR_PIN, INPUT);
    pinMode(VOLTAGE_SENSOR_PIN, INPUT);

#if DEBUG_MODE
    Serial.println("[SENSORS] Initialized");
#endif
}

// ==========================================================
// VOLTAGE READING
// ==========================================================

float SensorManager::readVoltage()
{
    long adcSum = 0;

    for (int i = 0; i < SENSOR_SAMPLE_COUNT; i++)
    {
        adcSum += analogRead(VOLTAGE_SENSOR_PIN);
        delayMicroseconds(100);
    }

    int averageADC = adcSum / SENSOR_SAMPLE_COUNT;

    return calculateVoltage(averageADC);
}

// ==========================================================
// CURRENT READING
// ==========================================================

float SensorManager::readCurrent()
{
    long adcSum = 0;

    for (int i = 0; i < SENSOR_SAMPLE_COUNT; i++)
    {
        adcSum += analogRead(CURRENT_SENSOR_PIN);
        delayMicroseconds(100);
    }

    int averageADC = adcSum / SENSOR_SAMPLE_COUNT;

    return calculateCurrent(averageADC);
}

// ==========================================================
// POWER FACTOR
// ==========================================================

float SensorManager::readPowerFactor()
{
    return DEFAULT_POWER_FACTOR;
}

// ==========================================================
// COMBINED SENSOR READING
// ==========================================================

SensorData SensorManager::readAll()
{
    SensorData data;

    data.voltage = readVoltage();
    data.current = readCurrent();
    data.powerFactor = readPowerFactor();

    data.timestamp = millis();

    return data;
}

// ==========================================================
// RAW ADC READS
// ==========================================================

int SensorManager::readVoltageADC()
{
    return analogRead(VOLTAGE_SENSOR_PIN);
}

int SensorManager::readCurrentADC()
{
    return analogRead(CURRENT_SENSOR_PIN);
}

// ==========================================================
// VOLTAGE CONVERSION
// ==========================================================

float SensorManager::calculateVoltage(
    int adcValue
)
{
    float sensorVoltage =
        (adcValue * ADC_REFERENCE_VOLTAGE)
        / ADC_RESOLUTION;

    float mainsVoltage =
        sensorVoltage *
        VOLTAGE_CALIBRATION_FACTOR;

    return mainsVoltage;
}

// ==========================================================
// CURRENT CONVERSION
// ==========================================================

float SensorManager::calculateCurrent(
    int adcValue
)
{
    float sensorVoltage =
        (adcValue * ADC_REFERENCE_VOLTAGE)
        / ADC_RESOLUTION;

    float current =
        (sensorVoltage - ACS712_ZERO_CURRENT)
        / ACS712_SENSITIVITY;

    current = fabs(current);

    return current;
}

// ==========================================================
// HELPER FUNCTIONS
// ==========================================================

float getVoltageReading()
{
    return Sensors.readVoltage();
}

float getCurrentReading()
{
    return Sensors.readCurrent();
}

float getPowerFactorReading()
{
    return Sensors.readPowerFactor();
}

SensorData getSensorData()
{
    return Sensors.readAll();
}

// ==========================================================
// DEBUG PRINT
// ==========================================================

void printSensorData(
    const SensorData& data
)
{
#if DEBUG_MODE

    Serial.println();
    Serial.println("========== SENSOR DATA ==========");

    Serial.print("Voltage: ");
    Serial.print(data.voltage);
    Serial.println(" V");

    Serial.print("Current: ");
    Serial.print(data.current);
    Serial.println(" A");

    Serial.print("Power Factor: ");
    Serial.println(data.powerFactor);

    Serial.print("Timestamp: ");
    Serial.println(data.timestamp);

    Serial.println("=================================");
    Serial.println();

#endif
}

/*
==========================================================
END OF FILE
==========================================================
*/