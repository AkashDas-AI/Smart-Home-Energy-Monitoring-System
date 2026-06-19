/*
==========================================================
Smart Home Energy Monitoring System
energy_calc.cpp
==========================================================

Purpose:
Implements power, energy, and cost calculations.

Calculations:

Apparent Power (VA)
S = V × I

Active Power (W)
P = V × I × PF

Reactive Power (VAR)
Q = √(S² − P²)

Energy (kWh)
(Power × Time) / 1000

Author: Akash Das
==========================================================
*/

#include "energy_calc.h"

#include <math.h>

// ==========================================================
// CONFIGURATION
// ==========================================================

// Electricity tariff (₹ per kWh)

static constexpr float ELECTRICITY_RATE = 8.0f;

// ==========================================================
// GLOBAL INSTANCE
// ==========================================================

EnergyCalculator Energy;

// ==========================================================
// CONSTRUCTOR
// ==========================================================

EnergyCalculator::EnergyCalculator()
{
    totalEnergyKWh = 0.0f;
}

// ==========================================================
// APPARENT POWER
// ==========================================================

float EnergyCalculator::calculateApparentPower(
    float voltage,
    float current
)
{
    return voltage * current;
}

// ==========================================================
// ACTIVE POWER
// ==========================================================

float EnergyCalculator::calculateActivePower(
    float voltage,
    float current,
    float powerFactor
)
{
    return voltage * current * powerFactor;
}

// ==========================================================
// REACTIVE POWER
// ==========================================================

float EnergyCalculator::calculateReactivePower(
    float apparentPower,
    float activePower
)
{
    float value =
        (apparentPower * apparentPower) -
        (activePower * activePower);

    if (value < 0.0f)
    {
        value = 0.0f;
    }

    return sqrt(value);
}

// ==========================================================
// ENERGY TRACKING
// ==========================================================

float EnergyCalculator::updateEnergyConsumption(
    float activePowerW,
    float elapsedSeconds
)
{
    float energyKWh =
        (activePowerW * elapsedSeconds)
        / 3600000.0f;

    totalEnergyKWh += energyKWh;

    return totalEnergyKWh;
}

// ==========================================================
// GET TOTAL ENERGY
// ==========================================================

float EnergyCalculator::getTotalEnergyKWh()
{
    return totalEnergyKWh;
}

// ==========================================================
// RESET COUNTER
// ==========================================================

void EnergyCalculator::resetEnergyCounter()
{
    totalEnergyKWh = 0.0f;
}

// ==========================================================
// COST CALCULATION
// ==========================================================

float EnergyCalculator::calculateCost(
    float energyKWh
)
{
    return energyKWh * ELECTRICITY_RATE;
}

// ==========================================================
// COMBINED CALCULATION
// ==========================================================

EnergyData EnergyCalculator::calculate(
    float voltage,
    float current,
    float powerFactor,
    float elapsedSeconds
)
{
    EnergyData data;

    data.apparentPowerVA =
        calculateApparentPower(
            voltage,
            current
        );

    data.activePowerW =
        calculateActivePower(
            voltage,
            current,
            powerFactor
        );

    data.reactivePowerVAR =
        calculateReactivePower(
            data.apparentPowerVA,
            data.activePowerW
        );

    data.energyKWh =
        updateEnergyConsumption(
            data.activePowerW,
            elapsedSeconds
        );

    data.estimatedCost =
        calculateCost(
            data.energyKWh
        );

    data.timestamp = millis();

    return data;
}

// ==========================================================
// HELPER FUNCTIONS
// ==========================================================

float calculateApparentPower(
    float voltage,
    float current
)
{
    return voltage * current;
}

float calculateActivePower(
    float voltage,
    float current,
    float powerFactor
)
{
    return voltage * current * powerFactor;
}

float calculateReactivePower(
    float apparentPower,
    float activePower
)
{
    float value =
        (apparentPower * apparentPower) -
        (activePower * activePower);

    if (value < 0.0f)
    {
        value = 0.0f;
    }

    return sqrt(value);
}

float calculateEnergyKWh(
    float activePowerW,
    float elapsedSeconds
)
{
    return
        (activePowerW * elapsedSeconds)
        / 3600000.0f;
}

// ==========================================================
// DEBUG OUTPUT
// ==========================================================

void printEnergyData(
    const EnergyData& data
)
{
    Serial.println();
    Serial.println("========== ENERGY DATA ==========");

    Serial.print("Apparent Power: ");
    Serial.print(data.apparentPowerVA);
    Serial.println(" VA");

    Serial.print("Active Power: ");
    Serial.print(data.activePowerW);
    Serial.println(" W");

    Serial.print("Reactive Power: ");
    Serial.print(data.reactivePowerVAR);
    Serial.println(" VAR");

    Serial.print("Energy: ");
    Serial.print(data.energyKWh, 6);
    Serial.println(" kWh");

    Serial.print("Cost: INR ");
    Serial.println(data.estimatedCost, 2);

    Serial.println("=================================");
    Serial.println();
}

/*
==========================================================
END OF FILE
==========================================================
*/