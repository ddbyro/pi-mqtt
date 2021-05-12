#!/usr/bin/env python3
import paho.mqtt.client as mqtt_client
import time
import RPi.GPIO as GPIO


mqtt_broker = "192.168.0.191"
mqtt_port = 1883
mqtt_topic = "hackdays/test"
client_id = 'pi-mqtt'
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.OUT)


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client()
    # client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(mqtt_broker, mqtt_port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = "hello"
        result = client.publish(mqtt_topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{mqtt_topic}`")
        else:
            print(f"Failed to send message to topic {mqtt_topic}")
        msg_count += 1


def get_gpio_state():
    GPIO.input(18)

def main():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    main()
