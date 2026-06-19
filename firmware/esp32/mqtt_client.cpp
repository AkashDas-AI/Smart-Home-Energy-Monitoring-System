/*
==========================================================
Smart Home Energy Monitoring System
mqtt_client.cpp
==========================================================

Purpose:
Handles:

- Wi-Fi Connection
- MQTT Connection
- MQTT Reconnection
- Telemetry Publishing
- Alert Publishing
- Status Publishing

Publishes Data To:

home/energy/node1/telemetry
home/energy/node1/alerts
home/energy/node1/status

Dependencies:

- WiFi.h
- PubSubClient.h
- ArduinoJson.h

Required Libraries:

PubSubClient
ArduinoJson

Author: Akash Das
==========================================================
*/

#include "config.h"
#include "alerts.h"
#include "energy_calc.h"
#include "sensors.h"

#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// ==========================================================
// GLOBAL OBJECTS
// ==========================================================

WiFiClient wifiClient;

PubSubClient mqttClient(
    wifiClient
);

// ==========================================================
// WIFI CONNECTION
// ==========================================================

void connectWiFi()
{
    Serial.println();
    Serial.println("================================");
    Serial.println("Connecting to WiFi...");
    Serial.println("================================");

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println();
    Serial.println("WiFi Connected");

    Serial.print("IP Address: ");
    Serial.println(
        WiFi.localIP()
    );

    Serial.println();
}

// ==========================================================
// MQTT CALLBACK
// ==========================================================

void mqttCallback(
    char* topic,
    byte* payload,
    unsigned int length
)
{
    Serial.print("[MQTT] Message Received: ");

    Serial.println(topic);
}

// ==========================================================
// MQTT CONNECT
// ==========================================================

bool connectMQTT()
{
    if (mqttClient.connected())
    {
        return true;
    }

    Serial.println();
    Serial.println("Connecting to MQTT Broker...");

    String clientId =
        String(DEVICE_ID) +
        "_" +
        String(random(1000));

    bool connected =
        mqttClient.connect(
            clientId.c_str()
        );

    if (connected)
    {
        Serial.println(
            "MQTT Connected"
        );

        publishStatus("ONLINE");
    }
    else
    {
        Serial.print(
            "MQTT Connection Failed. State="
        );

        Serial.println(
            mqttClient.state()
        );
    }

    return connected;
}

// ==========================================================
// MQTT SETUP
// ==========================================================

void setupMQTT()
{
    mqttClient.setServer(
        MQTT_BROKER,
        MQTT_PORT
    );

    mqttClient.setCallback(
        mqttCallback
    );
}

// ==========================================================
// MQTT LOOP
// ==========================================================

void mqttLoop()
{
    if (!mqttClient.connected())
    {
        connectMQTT();
    }

    mqttClient.loop();
}

// ==========================================================
// STATUS PUBLISH
// ==========================================================

bool publishStatus(
    const String& status
)
{
    StaticJsonDocument<256> doc;

    doc["device_id"] = DEVICE_ID;
    doc["status"] = status;
    doc["timestamp"] = millis();

    char buffer[256];

    serializeJson(
        doc,
        buffer
    );

    return mqttClient.publish(
        MQTT_STATUS_TOPIC,
        buffer,
        true
    );
}

// ==========================================================
// ALERT PUBLISH
// ==========================================================

bool publishAlert(
    const AlertStatus& alert
)
{
    StaticJsonDocument<512> doc;

    doc["device_id"] = DEVICE_ID;

    doc["alert_type"] =
        alertTypeToString(
            alert.type
        );

    doc["severity"] =
        severityToString(
            alert.severity
        );

    doc["message"] =
        alert.message;

    doc["timestamp"] =
        alert.timestamp;

    char buffer[512];

    serializeJson(
        doc,
        buffer
    );

    return mqttClient.publish(
        MQTT_ALERT_TOPIC,
        buffer
    );
}

// ==========================================================
// TELEMETRY PUBLISH
// ==========================================================

bool publishTelemetry(
    const SensorData& sensorData,
    const EnergyData& energyData,
    const AlertStatus& alertStatus
)
{
    StaticJsonDocument<
        MQTT_JSON_BUFFER_SIZE
    > doc;

    doc["device_id"] = DEVICE_ID;

    doc["voltage"] =
        sensorData.voltage;

    doc["current"] =
        sensorData.current;

    doc["power_factor"] =
        sensorData.powerFactor;

    doc["apparent_power_va"] =
        energyData.apparentPowerVA;

    doc["active_power_w"] =
        energyData.activePowerW;

    doc["reactive_power_var"] =
        energyData.reactivePowerVAR;

    doc["energy_kwh"] =
        energyData.energyKWh;

    doc["estimated_cost"] =
        energyData.estimatedCost;

    doc["alert_status"] =
        alertStatus.alertActive
        ? "ALERT"
        : "NORMAL";

    doc["alert_type"] =
        alertTypeToString(
            alertStatus.type
        );

    doc["severity"] =
        severityToString(
            alertStatus.severity
        );

    doc["timestamp"] =
        millis();

    char buffer[
        MQTT_JSON_BUFFER_SIZE
    ];

    serializeJson(
        doc,
        buffer
    );

    return mqttClient.publish(
        MQTT_TELEMETRY_TOPIC,
        buffer
    );
}

// ==========================================================
// DISCONNECT
// ==========================================================

void disconnectMQTT()
{
    publishStatus(
        "OFFLINE"
    );

    delay(500);

    mqttClient.disconnect();

    Serial.println(
        "[MQTT] Disconnected"
    );
}

/*
==========================================================
USAGE EXAMPLE

connectWiFi();

setupMQTT();

connectMQTT();

publishTelemetry(
    sensorData,
    energyData,
    alertStatus
);

==========================================================
END OF FILE
==========================================================
*/