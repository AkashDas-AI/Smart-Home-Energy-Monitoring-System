/*
==========================================================
Smart Home Energy Monitoring System
sensors.h
==========================================================

Purpose:
Provides sensor interfaces for reading:

- Voltage Sensor
- ACS712 Current Sensor

Also provides helper functions for:

- Sensor initialization
- Voltage calculation
- Current calculation
- Power factor retrieval
- Raw ADC diagnostics

Used By:
- main.ino
- energy_calc.cpp
- alerts.cpp

Author: Akash Das
==========================================================
*/

#ifndef SENSORS_H
#define SENSORS_H

#include <Arduino.h>

// ==========================================================
// SENSOR DATA STRUCTURE
// ==========================================================

struct SensorData
{
    float voltage;
    float current;
    float powerFactor;

    unsigned long timestamp;
};

// ==========================================================
// SENSOR MANAGER CLASS
// ==========================================================

class SensorManager
{
public:

    SensorManager();

    // --------------------------------------
    // Initialization
    // --------------------------------------

    void begin();

    // --------------------------------------
    // Individual Measurements
    // --------------------------------------

    float readVoltage();

    float readCurrent();

    float readPowerFactor();

    // --------------------------------------
    // Combined Reading
    // --------------------------------------

    SensorData readAll();

    // --------------------------------------
    // Diagnostics
    // --------------------------------------

    int readVoltageADC();

    int readCurrentADC();

private:

    float calculateVoltage(
        int adcValue
    );

    float calculateCurrent(
        int adcValue
    );
};

// ==========================================================
// UTILITY FUNCTIONS
// ==========================================================

float getVoltageReading();

float getCurrentReading();

float getPowerFactorReading();

SensorData getSensorData();

// ==========================================================
// DEBUG UTILITIES
// ==========================================================

void printSensorData(
    const SensorData& data
);

// ==========================================================
// GLOBAL SENSOR INSTANCE
// ==========================================================

extern SensorManager Sensors;

#endif

/*
==========================================================
END OF FILE
==========================================================
*/