#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import yaml
import time
import RPi.GPIO as GPIO

config = yaml.full_load(open('./config.yaml'))

mqtt_broker = config['broker_configs']['host']
mqtt_port = config['broker_configs']['port']
mqtt_status_topic = config['relays'][0]['status_topic']
mqtt_set_topic = config['relays'][0]['set_topic']
gpio_pin = config['relays'][0]['pin']


def set_gpio_state(pin=None, state=None):
    GPIO.output(pin, state)


def get_gpio_state(pin=None):
    return GPIO.input(pin)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    # Subscribing to receive RPC requests
    # client.subscribe(mqtt_set_topic)
    for relay in config['relays']:
        # mqtt_set_topic.append(relay['set_topic'])
        client.subscribe(relay['set_topic'])


def on_publish(client, userdata, mid):
    print(f'published\'{get_gpio_state(pin=gpio_pin)}\' to \'{mqtt_status_topic}\'')



def on_message(client, userdata, msg):
    #print(f'Topic {msg.topic} Message: {msg.payload.decode()}')
    GPIO.setup(gpio_pin, GPIO.OUT)

    if msg.payload.decode() == '0':
        print('state set to \'off\'')
        set_gpio_state(pin=gpio_pin, state=GPIO.LOW)
        # GPIO.output(gpio_pin, state)

    if msg.payload.decode() == '1':
        print('state set to \'on\'')
        set_gpio_state(pin=gpio_pin, state=GPIO.HIGH)
        # GPIO.output(gpio_pin, GPIO.HIGH)
    for relay in config['relays']:
        gpio_pin = relay['pin']

        previous_state = ''

        if previous_state != get_gpio_state(pin=gpio_pin):
            client.publish(mqtt_status_topic, get_gpio_state(pin=gpio_pin))
            print(f'published \'{get_gpio_state(pin=gpio_pin)}\' to \'{mqtt_status_topic}\'')
            previous_state = get_gpio_state(pin=gpio_pin)


def connect_mqtt():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

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

