/*
==========================================================
Smart Home Energy Monitoring System
alerts.h
==========================================================

Purpose:
Provides alert monitoring and protection logic for:

- Overvoltage Detection
- Undervoltage Detection
- Overcurrent Detection
- Overload Detection
- High Energy Usage Detection

Also controls:

- Relay
- LEDs
- Buzzer

Author: Akash Das
==========================================================
*/

#ifndef ALERTS_H
#define ALERTS_H

#include <Arduino.h>

// ==========================================================
// ALERT TYPES
// ==========================================================

enum AlertType
{
    ALERT_NONE = 0,

    ALERT_OVERVOLTAGE,
    ALERT_UNDERVOLTAGE,

    ALERT_OVERCURRENT,

    ALERT_OVERLOAD,

    ALERT_HIGH_ENERGY_USAGE
};

// ==========================================================
// ALERT SEVERITY
// ==========================================================

enum AlertSeverity
{
    SEVERITY_NORMAL = 0,

    SEVERITY_WARNING,

    SEVERITY_CRITICAL
};

// ==========================================================
// ALERT RESULT STRUCTURE
// ==========================================================

struct AlertStatus
{
    bool alertActive;

    AlertType type;

    AlertSeverity severity;

    String message;

    unsigned long timestamp;
};

// ==========================================================
// ALERT MANAGER CLASS
// ==========================================================

class AlertManager
{
public:

    AlertManager();

    // --------------------------------------
    // Initialization
    // --------------------------------------

    void begin();

    // --------------------------------------
    // Voltage Checks
    // --------------------------------------

    AlertStatus checkVoltage(
        float voltage
    );

    // --------------------------------------
    // Current Checks
    // --------------------------------------

    AlertStatus checkCurrent(
        float current
    );

    // --------------------------------------
    // Power Checks
    // --------------------------------------

    AlertStatus checkPower(
        float activePowerW
    );

    // --------------------------------------
    // Energy Checks
    // --------------------------------------

    AlertStatus checkEnergy(
        float energyKWh
    );

    // --------------------------------------
    // Full System Evaluation
    // --------------------------------------

    AlertStatus evaluate(
        float voltage,
        float current,
        float activePower,
        float energyKWh
    );

    // --------------------------------------
    // Outputs
    // --------------------------------------

    void activateAlert(
        const AlertStatus& alert
    );

    void clearAlert();

    // --------------------------------------
    // Status
    // --------------------------------------

    bool isAlertActive();

    AlertStatus getCurrentAlert();

private:

    AlertStatus currentAlert;
};

// ==========================================================
// HELPER FUNCTIONS
// ==========================================================

String alertTypeToString(
    AlertType type
);

String severityToString(
    AlertSeverity severity
);

// ==========================================================
// DEBUG UTILITIES
// ==========================================================

void printAlertStatus(
    const AlertStatus& alert
);

// ==========================================================
// GLOBAL INSTANCE
// ==========================================================

extern AlertManager Alerts;

#endif

/*
==========================================================
END OF FILE
==========================================================
*/