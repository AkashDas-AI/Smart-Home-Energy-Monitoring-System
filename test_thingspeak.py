from dashboard.thingspeak import ThingSpeakClient

client = ThingSpeakClient()

success = client.publish_energy_data(
    voltage=230.5,
    current=4.2,
    power=966.1,
    energy_kwh=1.25,
    cost=10.00,
    power_factor=0.95,
    alert_count=0,
    status=1
)

print("Success:", success)