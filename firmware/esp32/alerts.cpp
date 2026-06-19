/*
==========================================================
Smart Home Energy Monitoring System
alerts.cpp
==========================================================

Purpose:
Implements alert monitoring and protection logic.

Monitors:

- Overvoltage
- Undervoltage
- Overcurrent
- Overload
- High Energy Usage

Controls:

- Relay
- LEDs
- Buzzer

Author: Akash Das
==========================================================
*/

#include "alerts.h"
#include "config.h"

// ==========================================================
// GLOBAL INSTANCE
// ==========================================================

AlertManager Alerts;

// ==========================================================
// CONSTRUCTOR
// ==========================================================

AlertManager::AlertManager()
{
    currentAlert.alertActive = false;
    currentAlert.type = ALERT_NONE;
    currentAlert.severity = SEVERITY_NORMAL;
    currentAlert.message = "System Normal";
    currentAlert.timestamp = 0;
}

// ==========================================================
// INITIALIZATION
// ==========================================================

void AlertManager::begin()
{
    pinMode(RELAY_PIN, OUTPUT);

    pinMode(GREEN_LED_PIN, OUTPUT);
    pinMode(YELLOW_LED_PIN, OUTPUT);
    pinMode(RED_LED_PIN, OUTPUT);

    pinMode(BUZZER_PIN, OUTPUT);

    clearAlert();

#if DEBUG_MODE
    Serial.println("[ALERTS] Initialized");
#endif
}

// ==========================================================
// VOLTAGE CHECK
// ==========================================================

AlertStatus AlertManager::checkVoltage(
    float voltage
)
{
    AlertStatus alert;

    alert.alertActive = false;
    alert.type = ALERT_NONE;
    alert.severity = SEVERITY_NORMAL;
    alert.message = "Voltage Normal";
    alert.timestamp = millis();

    if (voltage > MAX_VOLTAGE_THRESHOLD)
    {
        alert.alertActive = true;
        alert.type = ALERT_OVERVOLTAGE;
        alert.severity = SEVERITY_CRITICAL;
        alert.message = "Overvoltage Detected";
    }
    else if (voltage < MIN_VOLTAGE_THRESHOLD)
    {
        alert.alertActive = true;
        alert.type = ALERT_UNDERVOLTAGE;
        alert.severity = SEVERITY_CRITICAL;
        alert.message = "Undervoltage Detected";
    }

    return alert;
}

// ==========================================================
// CURRENT CHECK
// ==========================================================

AlertStatus AlertManager::checkCurrent(
    float current
)
{
    AlertStatus alert;

    alert.alertActive = false;
    alert.type = ALERT_NONE;
    alert.severity = SEVERITY_NORMAL;
    alert.message = "Current Normal";
    alert.timestamp = millis();

    if (current > MAX_CURRENT)
    {
        alert.alertActive = true;
        alert.type = ALERT_OVERCURRENT;
        alert.severity = SEVERITY_CRITICAL;
        alert.message = "Overcurrent Detected";
    }
    else if (current > WARNING_CURRENT)
    {
        alert.alertActive = true;
        alert.type = ALERT_OVERCURRENT;
        alert.severity = SEVERITY_WARNING;
        alert.message = "High Current Warning";
    }

    return alert;
}

// ==========================================================
// POWER CHECK
// ==========================================================

AlertStatus AlertManager::checkPower(
    float activePowerW
)
{
    AlertStatus alert;

    alert.alertActive = false;
    alert.type = ALERT_NONE;
    alert.severity = SEVERITY_NORMAL;
    alert.message = "Power Normal";
    alert.timestamp = millis();

    if (activePowerW > MAX_POWER)
    {
        alert.alertActive = true;
        alert.type = ALERT_OVERLOAD;
        alert.severity = SEVERITY_CRITICAL;
        alert.message = "Power Overload";
    }
    else if (activePowerW > WARNING_POWER)
    {
        alert.alertActive = true;
        alert.type = ALERT_OVERLOAD;
        alert.severity = SEVERITY_WARNING;
        alert.message = "High Power Consumption";
    }

    return alert;
}

// ==========================================================
// ENERGY CHECK
// ==========================================================

AlertStatus AlertManager::checkEnergy(
    float energyKWh
)
{
    AlertStatus alert;

    alert.alertActive = false;
    alert.type = ALERT_NONE;
    alert.severity = SEVERITY_NORMAL;
    alert.message = "Energy Normal";
    alert.timestamp = millis();

    if (energyKWh > DAILY_ENERGY_LIMIT)
    {
        alert.alertActive = true;
        alert.type = ALERT_HIGH_ENERGY_USAGE;
        alert.severity = SEVERITY_WARNING;
        alert.message = "High Daily Energy Usage";
    }

    return alert;
}

// ==========================================================
// COMPLETE EVALUATION
// ==========================================================

AlertStatus AlertManager::evaluate(
    float voltage,
    float current,
    float activePower,
    float energyKWh
)
{
    AlertStatus voltageAlert =
        checkVoltage(voltage);

    if (voltageAlert.alertActive)
        return voltageAlert;

    AlertStatus currentAlert =
        checkCurrent(current);

    if (currentAlert.alertActive)
        return currentAlert;

    AlertStatus powerAlert =
        checkPower(activePower);

    if (powerAlert.alertActive)
        return powerAlert;

    AlertStatus energyAlert =
        checkEnergy(energyKWh);

    if (energyAlert.alertActive)
        return energyAlert;

    AlertStatus normal;

    normal.alertActive = false;
    normal.type = ALERT_NONE;
    normal.severity = SEVERITY_NORMAL;
    normal.message = "System Normal";
    normal.timestamp = millis();

    return normal;
}

// ==========================================================
// ACTIVATE ALERT
// ==========================================================

void AlertManager::activateAlert(
    const AlertStatus& alert
)
{
    currentAlert = alert;

    digitalWrite(GREEN_LED_PIN, LOW);

    if (alert.severity == SEVERITY_WARNING)
    {
        digitalWrite(YELLOW_LED_PIN, HIGH);
        digitalWrite(RED_LED_PIN, LOW);
    }
    else
    {
        digitalWrite(YELLOW_LED_PIN, LOW);
        digitalWrite(RED_LED_PIN, HIGH);
    }

    tone(
        BUZZER_PIN,
        BUZZER_FREQUENCY,
        BUZZER_DURATION_MS
    );

    digitalWrite(
        RELAY_PIN,
        RELAY_ACTIVE_HIGH ? LOW : HIGH
    );

#if DEBUG_MODE
    printAlertStatus(alert);
#endif
}

// ==========================================================
// CLEAR ALERT
// ==========================================================

void AlertManager::clearAlert()
{
    currentAlert.alertActive = false;
    currentAlert.type = ALERT_NONE;
    currentAlert.severity = SEVERITY_NORMAL;
    currentAlert.message = "System Normal";
    currentAlert.timestamp = millis();

    digitalWrite(GREEN_LED_PIN, HIGH);
    digitalWrite(YELLOW_LED_PIN, LOW);
    digitalWrite(RED_LED_PIN, LOW);

    digitalWrite(
        RELAY_PIN,
        RELAY_ACTIVE_HIGH ? HIGH : LOW
    );
}

// ==========================================================
// STATUS METHODS
// ==========================================================

bool AlertManager::isAlertActive()
{
    return currentAlert.alertActive;
}

AlertStatus AlertManager::getCurrentAlert()
{
    return currentAlert;
}

// ==========================================================
// ALERT TYPE STRING
// ==========================================================

String alertTypeToString(
    AlertType type
)
{
    switch (type)
    {
        case ALERT_OVERVOLTAGE:
            return "OVERVOLTAGE";

        case ALERT_UNDERVOLTAGE:
            return "UNDERVOLTAGE";

        case ALERT_OVERCURRENT:
            return "OVERCURRENT";

        case ALERT_OVERLOAD:
            return "OVERLOAD";

        case ALERT_HIGH_ENERGY_USAGE:
            return "HIGH_ENERGY_USAGE";

        default:
            return "NONE";
    }
}

// ==========================================================
// SEVERITY STRING
// ==========================================================

String severityToString(
    AlertSeverity severity
)
{
    switch (severity)
    {
        case SEVERITY_WARNING:
            return "WARNING";

        case SEVERITY_CRITICAL:
            return "CRITICAL";

        default:
            return "NORMAL";
    }
}

// ==========================================================
// DEBUG PRINT
// ==========================================================

void printAlertStatus(
    const AlertStatus& alert
)
{
#if DEBUG_MODE

    Serial.println();
    Serial.println("========== ALERT ==========");

    Serial.print("Type: ");
    Serial.println(
        alertTypeToString(alert.type)
    );

    Serial.print("Severity: ");
    Serial.println(
        severityToString(alert.severity)
    );

    Serial.print("Message: ");
    Serial.println(alert.message);

    Serial.println("===========================");
    Serial.println();

#endif
}

/*
==========================================================
END OF FILE
==========================================================
*/