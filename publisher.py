import time
from network import WLAN
from machine import ADC
from umqtt.robust import MQTTClient

# =========================
# WiFi credentials
# =========================
SSID = "Moes iPhone"
PASSWORD = "moe2drizzy"

# =========================
# MQTT configuration
# =========================
MQTT_BROKER = "172.20.10.2"   # Raspberry Pi IP
MQTT_PORT = 1883
TOPIC = "temp/pico"
CLIENT_ID = b"pico_publisher"

# =========================
# WiFi connection
# =========================
def connect_wifi():
    wifi = WLAN(WLAN.IF_STA)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    print("Connecting to WiFi...")
    timeout = 15  # seconds

    while timeout > 0:
        if wifi.status() == 3:  # connected
            break
        time.sleep(1)
        timeout -= 1

    if wifi.status() != 3:
        raise Exception("WiFi failed to connect")

    print("Connected to WiFi")
    print("IP address:", wifi.ifconfig()[0])
    return wifi

# =========================
# MQTT connection
# =========================
def connect_mqtt():
    client = MQTTClient(
        client_id=CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=60,
    )

    client.connect()
    print("Connected to MQTT broker at", MQTT_BROKER)
    return client

# =========================
# Temperature reading
# =========================
def read_temperature(sensor):
    voltage = sensor.read_u16() * (3.3 / 65535)
    temperature = 27 - (voltage - 0.706) / 0.001721
    return temperature

# =========================
# Main program
# =========================
def main():
    temp_sensor = ADC(4)

    connect_wifi()
    mqtt = connect_mqtt()

    while True:
        temp = read_temperature(temp_sensor)
        mqtt.publish(TOPIC, f"{temp:.2f}".encode())
        print(f"Published temperature: {temp:.2f} °C")
        time.sleep(0.5)

# =========================
# Run
# =========================
if __name__ == "__main__":
    main()


