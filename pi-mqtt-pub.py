#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import yaml
import RPi.GPIO as GPIO

config = yaml.full_load(open('./config.yaml'))

mqtt_broker = config['configs']['host']
mqtt_port = config['configs']['port']
mqtt_topic = config['configs']['relays']['relay01']['status_topic']

gpio_pin = config['configs']['relays']['relay01']['pin']


def get_gpio_state(pin=None):
    return GPIO.input(pin)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')


def on_publish(client, userdata, mid):
    print(f'published \'{get_gpio_state(pin=gpio_pin)}\' to \'{mqtt_topic}\'')


def connect_mqtt():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect(mqtt_broker, mqtt_port, 60)

    previous_state = ''
    while True:
        if previous_state != get_gpio_state(pin=gpio_pin):
            client.publish(mqtt_topic, get_gpio_state(pin=gpio_pin))
            previous_state = get_gpio_state(pin=gpio_pin)

    client.loop_forever()


def main():
    try:
        connect_mqtt()
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
   main()

