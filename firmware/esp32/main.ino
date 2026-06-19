/*
==========================================================
Smart Home Energy Monitoring System
main.ino
==========================================================

Purpose:
Main ESP32 application entry point.

Responsibilities:

- Initialize hardware
- Read sensors
- Calculate power metrics
- Evaluate alerts
- Publish MQTT telemetry
- Publish MQTT alerts
- Maintain MQTT connection

Author: Akash Das
==========================================================
*/

#include "config.h"
#include "sensors.h"
#include "energy_calc.h"
#include "alerts.h"

// MQTT functions from mqtt_client.cpp

void connectWiFi();
void setupMQTT();
bool connectMQTT();
void mqttLoop();

bool publishStatus(
    const String& status
);

bool publishAlert(
    const AlertStatus& alert
);

bool publishTelemetry(
    const SensorData& sensorData,
    const EnergyData& energyData,
    const AlertStatus& alertStatus
);

void disconnectMQTT();

// ==========================================================
// GLOBAL VARIABLES
// ==========================================================

unsigned long lastTelemetryTime = 0;

unsigned long previousLoopTime = 0;

// ==========================================================
// STARTUP BANNER
// ==========================================================

void printStartupBanner()
{
    Serial.println();
    Serial.println("==================================================");
    Serial.println("SMART HOME ENERGY MONITORING SYSTEM");
    Serial.println("ESP32 ENERGY NODE");
    Serial.println("==================================================");

    Serial.print("Device ID: ");
    Serial.println(DEVICE_ID);

    Serial.print("Location: ");
    Serial.println(DEVICE_LOCATION);

    Serial.println("==================================================");
    Serial.println();
}

// ==========================================================
// SETUP
// ==========================================================

void setup()
{
    Serial.begin(
        SERIAL_BAUD_RATE
    );

    delay(1000);

    printStartupBanner();

    // --------------------------------------
    // Initialize Modules
    // --------------------------------------

    Sensors.begin();

    Alerts.begin();

    Energy.resetEnergyCounter();

    // --------------------------------------
    // Network
    // --------------------------------------

    connectWiFi();

    setupMQTT();

    connectMQTT();

    publishStatus(
        "ONLINE"
    );

    previousLoopTime = millis();

    Serial.println();
    Serial.println("[SYSTEM] Ready");
    Serial.println();
}

// ==========================================================
// PROCESS ENERGY CYCLE
// ==========================================================

void processEnergyMonitoring()
{
    unsigned long currentTime =
        millis();

    float elapsedSeconds =
        (currentTime - previousLoopTime)
        / 1000.0f;

    previousLoopTime =
        currentTime;

    // --------------------------------------
    // Read Sensors
    // --------------------------------------

    SensorData sensorData =
        Sensors.readAll();

    // --------------------------------------
    // Calculate Energy Metrics
    // --------------------------------------

    EnergyData energyData =
        Energy.calculate(
            sensorData.voltage,
            sensorData.current,
            sensorData.powerFactor,
            elapsedSeconds
        );

    // --------------------------------------
    // Evaluate Alerts
    // --------------------------------------

    AlertStatus alertStatus =
        Alerts.evaluate(
            sensorData.voltage,
            sensorData.current,
            energyData.activePowerW,
            energyData.energyKWh
        );

    if (alertStatus.alertActive)
    {
        Alerts.activateAlert(
            alertStatus
        );

        publishAlert(
            alertStatus
        );
    }
    else
    {
        Alerts.clearAlert();
    }

    // --------------------------------------
    // Publish MQTT Telemetry
    // --------------------------------------

    publishTelemetry(
        sensorData,
        energyData,
        alertStatus
    );

    // --------------------------------------
    // Debug Output
    // --------------------------------------

#if DEBUG_MODE

    Serial.println(
        "--------------------------------------"
    );

    Serial.print("Voltage: ");
    Serial.print(sensorData.voltage);
    Serial.println(" V");

    Serial.print("Current: ");
    Serial.print(sensorData.current);
    Serial.println(" A");

    Serial.print("Power: ");
    Serial.print(energyData.activePowerW);
    Serial.println(" W");

    Serial.print("Energy: ");
    Serial.print(
        energyData.energyKWh,
        6
    );
    Serial.println(" kWh");

    Serial.print("Cost: INR ");
    Serial.println(
        energyData.estimatedCost,
        2
    );

    Serial.print("Alert: ");
    Serial.println(
        alertStatus.alertActive
        ? alertStatus.message
        : "NORMAL"
    );

    Serial.println(
        "--------------------------------------"
    );
    Serial.println();

#endif
}

// ==========================================================
// MAIN LOOP
// ==========================================================

void loop()
{
    mqttLoop();

    unsigned long currentTime =
        millis();

    if (
        currentTime -
        lastTelemetryTime >=
        TELEMETRY_INTERVAL_MS
    )
    {
        processEnergyMonitoring();

        lastTelemetryTime =
            currentTime;
    }
}

// ==========================================================
// END OF FILE
// ==========================================================