#!/usr/bin/env python3.7
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import yaml
import argparse
# from RPiSim.GPIO import GPIO

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', action='store', dest='path', help='Path to config.yaml.')

args = parser.parse_args()
config_path = args.path

config = yaml.full_load(open(config_path))

mqtt_broker = config['broker_configs']['host']
mqtt_port = config['broker_configs']['port']
mqtt_topic = config["broker_configs"]["topic"]
gpio_configs = config["gpio_configs"]


def set_gpio_state(pin=None, state=None):
    GPIO.setup(pin, state)


def get_gpio_state(pin=None):
    return GPIO.input(pin)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    for gpio in gpio_configs:
        client.subscribe(f'{mqtt_topic}/{gpio["id"]}/state')


def on_message(client, userdata, msg):
    print(f'Topic {msg.topic} Message: {msg.payload.decode()}')

    for gpio in gpio_configs:
        gpio_id = msg.topic.split("/")[-2]
        topic_message = msg.payload.decode()

        if f'{gpio_id}' in gpio["id"]:
            gpio_pin = gpio["pin"]

            if topic_message == 'off':
                GPIO.output(gpio_pin, GPIO.LOW)
                print(f'gpio pi {gpio_pin} state set to \'off\'')
                client.publish(f'{mqtt_topic}/{gpio["id"]}/status', get_gpio_state(pin=gpio_pin))
                if get_gpio_state(pin=gpio_pin) == 0:
                    client.publish(f'{mqtt_topic}/{gpio["id"]}/status', 'off')

            if topic_message == 'on':
                GPIO.output(gpio_pin, GPIO.HIGH)
                print(f'gpio pi {gpio_pin} state set to \'on\'')
                client.publish(f'{mqtt_topic}/{gpio["id"]}/status', get_gpio_state(pin=gpio_pin))
                if get_gpio_state(pin=gpio_pin) == 1:
                    client.publish(f'{mqtt_topic}/{gpio["id"]}/status', 'on')


def connect_mqtt():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for gpio in gpio_configs:
        GPIO.setup(gpio['pin'], GPIO.OUT)
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
