#!/usr/bin/env python3
import paho.mqtt.client as mqtt
# import RPi.GPIO as GPIO
import yaml

config = yaml.full_load(open('./config.yaml'))

mqtt_broker = config['mqtt_configs']['broker01']['host']
mqtt_port = config['mqtt_configs']['broker01']['port']
mqtt_topic = config['mqtt_configs']['broker01']['topic']

gpio_pin = config['gpio_configs']['pin']


def set_gpio_state(pin=None, state=None):
    GPIO.output(pin, state)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    # Subscribing to receive RPC requests
    client.subscribe(mqtt_topic)


def on_message(client, userdata, msg):
    print(f'Topic: {msg.topic}\nMessage: {msg.payload.decode()}')
    if msg.payload.decode() == '0':
        print('off')
        set_gpio_state(pin=gpio_pin, state=GPIO.LOW)
        # GPIO.output(gpio_pin, state)
    if msg.payload.decode() == '1':
        print('on')
        set_gpio_state(pin=gpio_pin, state=GPIO.HIGH)
        # GPIO.output(gpio_pin, GPIO.HIGH)


def connect_mqtt():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()


def main():
    try:
        connect_mqtt()
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    main()

