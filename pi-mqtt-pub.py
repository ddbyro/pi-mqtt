#!/usr/bin/env python3
import paho.mqtt.client as mqtt_client
import time
import RPi.GPIO as GPIO


mqtt_broker = "192.168.0.191"
mqtt_port = 1883
mqtt_topic = "hackdays/test"
client_id = 'pi-mqtt'
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)

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
    #msg_count = 0
    while True:
        time.sleep(.5)
        if get_gpio_state():
            msg = get_gpio_state()
        else:
            msg = get_gpio_state()
        result = client.publish(mqtt_topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{mqtt_topic}`")
        else:
            print(f"Failed to send message to topic {mqtt_topic}")
        #msg_count += 1


def get_gpio_state():
    state = GPIO.input(18)
    return state

def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn motor on


def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn motor off


def motor(pin=None, state=None):
    GPIO.output(pin, state)

def motor_on(pin):
    GPIO.output(pin, GPIO.HIGH)  # Turn motor on


def motor_off(pin):
    GPIO.output(pin, GPIO.LOW)  # Turn motor off


def motor(pin=None, state=None):
    GPIO.output(pin, state)


def main():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    main()
    #if get_gpio_state():
        #print(f'on - {get_gpio_state()}')
    #else:
        #print(f'off - {get_gpio_state()}')
    #GPIO.cleanup()
