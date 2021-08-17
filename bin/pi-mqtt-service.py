#!/usr/bin/env python3.7
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import yaml
import argparse
# from RPiSim.GPIO import GPIO  # this is used for debugging on a non-raspberry pi machine

# Setup commandline arguments for configs
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', action='store', dest='path', help='Path to config.yaml.')

args = parser.parse_args()
config_path = args.path

# Pull in config.yaml
config = yaml.full_load(open(config_path))

# global variables for configs
mqtt_broker = config['broker_configs']['host']
mqtt_port = config['broker_configs']['port']
mqtt_topic = config["broker_configs"]["topic"]
gpio_configs = config["gpio_configs"]


def set_gpio_state(pin=None, state=None):
    # set the gpio pin state
    GPIO.setup(pin, state)


def get_gpio_state(pin=None):
    # get the gpio state
    return GPIO.input(pin)


def on_connect(client, userdata, flags, rc):
    # execute on connect to mqtt
    print(f'Connected with result code {str(rc)}')
    # subscribe to each topic in topic config
    for gpio in gpio_configs:
        client.subscribe(f'{mqtt_topic}/{gpio["id"]}/state')


def on_message(client, userdata, msg):
    # execute on message update to subscribed topics
    print(f'Topic {msg.topic} Message: {msg.payload.decode()}')

    # set pin to published state and publish actual pin state to status topic
    for gpio in gpio_configs:
        gpio_id = msg.topic.split("/")[-2]
        topic_message = msg.payload.decode()

        if f'{gpio_id}' in gpio["id"]:
            gpio_pin = gpio["pin"]

            # set gpio to to LOW if topic state is 'off' or HIGH if state is 'on'
            if topic_message == 'off':
                # TODO : set output via config file for differing "Normal-open"/"Normal-closed" relays
                GPIO.output(gpio_pin, GPIO.LOW)
                print(f'gpio pi {gpio_pin} state set to \'off\'')

                # set gpio to 'off'
                client.publish(f'{mqtt_topic}/{gpio["id"]}/status', get_gpio_state(pin=gpio_pin))

                # publish pin state to status message
                if get_gpio_state(pin=gpio_pin) == 0:
                    client.publish(f'{mqtt_topic}/{gpio["id"]}/status', 'off')

            if topic_message == 'on':
                # TODO : set output via config file for differing "Normal-open"/"Normal-closed" relays
                GPIO.output(gpio_pin, GPIO.HIGH)
                print(f'gpio pi {gpio_pin} state set to \'on\'')

                # set gpio to 'on'
                client.publish(f'{mqtt_topic}/{gpio["id"]}/status', get_gpio_state(pin=gpio_pin))

                # publish pin state to status message
                if get_gpio_state(pin=gpio_pin) == 1:
                    client.publish(f'{mqtt_topic}/{gpio["id"]}/status', 'on')


def main():
    try:
        # setup gpio
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        for gpio in gpio_configs:
            GPIO.setup(gpio['pin'], GPIO.OUT)
        # connection loop for mqtt client
        client = mqtt.Client()
        client.on_connect = on_connect  # on connection run the on_connect function
        client.on_message = on_message  # on message published to subscribed topics run on_message function
        client.connect(mqtt_broker, mqtt_port, 60)  # connection string for mqtt broker
        client.loop_forever()  # loop subscriptions forever
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
