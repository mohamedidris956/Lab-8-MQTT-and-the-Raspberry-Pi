import time
from network import WLAN
from machine import ADC
from umqtt.robust import MQTTClient

SSID = "Moes iPhone"
PASSWORD = "moe2drizzy"

MQTT_BROKER = "172.20.10.2"
MQTT_PORT = 1883
TOPIC = "temp/pico"
CLIENT_ID = b"publish"

def connect_wifi():
    wifi = WLAN(WLAN.IF_STA)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)

    if wifi.status() != 3:
        raise Exception("WiFi failed to connect")

    print("Connected to WiFi")
    print("IP:", wifi.ifconfig()[0])


def connect_mqtt():
    mqtt = MQTTClient(
        client_id=CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=60,
    )

    mqtt.connect()
    print(f"Connected to MQTT broker at {MQTT_BROKER}")
    return mqtt


def read_temperature(temp_sensor):
    voltage = temp_sensor.read_u16() * (3.3 / 65535)
    temp = 27 - (voltage - 0.706) / 0.001721
    return temp


def publish_temperature(mqtt, temp_sensor):
    temp = read_temperature(temp_sensor)
    mqtt.publish(TOPIC, str(temp).encode())

    print(f"Sent: {temp:.2f}°C")
    time.sleep(0.5)


if __name__ == "__main__":
    temp_sensor = ADC(4)

    connect_wifi()
    mqtt = connect_mqtt()

    while True:
        publish_temperature(mqtt, temp_sensor)
