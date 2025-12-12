import time
import network
from machine import Pin
from umqtt.robust import MQTTClient

SSID = "Moes iPhone"
PASSWORD = "moe2drizzy"

MQTT_BROKER = "172.20.10.2"   # Pi IP on hotspot
MQTT_PORT = 1883
TOPIC = b"temp/pico"
CLIENT_ID = b"subscribe"

Built-in LED on Pico W
led = Pin("LED", Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to WiFi...")
    for i in range(20):
        if wlan.isconnected():
            print("Connected to WiFi")
            print("IP:", wlan.ifconfig()[0])
            return wlan
        time.sleep(1)

    raise RuntimeError("WiFi failed to connect")

def mqtt_callback(topic, msg):
    try:
        temp = float(msg)  # msg is bytes but float() can parse it if it's like b"23.4"
        print("Temperature received:", temp, "°C")

        if temp > 23:
            print("Temperature too high! Turning ON LED.")
            led.value(1)
        else:
            print("Temperature normal. Turning OFF LED.")
            led.value(0)

    except Exception as e:
        print("Error parsing message:", e)

def connect_mqtt():
    mqtt = MQTTClient(
        client_id=CLIENT_ID,
        server=MQTT_BROKER,
        port=MQTT_PORT,
        keepalive=7000,
    )

    mqtt.set_callback(mqtt_callback)
    mqtt.connect()
    print("Connected to MQTT broker at {}:{}".format(MQTT_BROKER, MQTT_PORT))

    mqtt.subscribe(TOPIC)
    print("Subscribed to topic:", TOPIC)

    return mqtt

if name == "main":
    connect_wifi()
    mqtt = connect_mqtt()

    while True:
        mqtt.wait_msg()

