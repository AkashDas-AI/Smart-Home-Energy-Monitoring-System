/*
==========================================================
Smart Home Energy Monitoring System
energy_calc.h
==========================================================

Purpose:
Provides electrical calculations for:

- Apparent Power (VA)
- Active Power (W)
- Reactive Power (VAR)
- Energy Consumption (kWh)
- Cost Estimation

Formulas:

S = V × I

P = V × I × PF

Q = √(S² − P²)

Energy(kWh) =
(Power × Time) / 1000

Author: Akash Das
==========================================================
*/

#ifndef ENERGY_CALC_H
#define ENERGY_CALC_H

#include <Arduino.h>

// ==========================================================
// ENERGY DATA STRUCTURE
// ==========================================================

struct EnergyData
{
    float apparentPowerVA;
    float activePowerW;
    float reactivePowerVAR;

    float energyKWh;

    float estimatedCost;

    unsigned long timestamp;
};

// ==========================================================
// ENERGY CALCULATOR CLASS
// ==========================================================

class EnergyCalculator
{
public:

    EnergyCalculator();

    // --------------------------------------
    // Power Calculations
    // --------------------------------------

    float calculateApparentPower(
        float voltage,
        float current
    );

    float calculateActivePower(
        float voltage,
        float current,
        float powerFactor
    );

    float calculateReactivePower(
        float apparentPower,
        float activePower
    );

    // --------------------------------------
    // Energy Tracking
    // --------------------------------------

    float updateEnergyConsumption(
        float activePowerW,
        float elapsedSeconds
    );

    float getTotalEnergyKWh();

    void resetEnergyCounter();

    // --------------------------------------
    // Cost Calculation
    // --------------------------------------

    float calculateCost(
        float energyKWh
    );

    // --------------------------------------
    // Combined Calculation
    // --------------------------------------

    EnergyData calculate(
        float voltage,
        float current,
        float powerFactor,
        float elapsedSeconds
    );

private:

    float totalEnergyKWh;
};

// ==========================================================
// HELPER FUNCTIONS
// ==========================================================

float calculateApparentPower(
    float voltage,
    float current
);

float calculateActivePower(
    float voltage,
    float current,
    float powerFactor
);

float calculateReactivePower(
    float apparentPower,
    float activePower
);

float calculateEnergyKWh(
    float activePowerW,
    float elapsedSeconds
);

// ==========================================================
// GLOBAL INSTANCE
// ==========================================================

extern EnergyCalculator Energy;

// ==========================================================
// DEBUG UTILITIES
// ==========================================================

void printEnergyData(
    const EnergyData& data
);

#endif

/*
==========================================================
END OF FILE
==========================================================
*/