#!/usr/bin/env python3.7
import paho.mqtt.client as mqtt
import yaml
# from RPiSim.GPIO import GPIO
import RPi.GPIO as GPIO

config = yaml.full_load(open('./config.yaml'))

mqtt_broker = config['broker_configs']['host']
mqtt_port = config['broker_configs']['port']


def set_gpio_state(pin=None, state=None):
    GPIO.setup(pin, state)


def get_gpio_state(pin=None):
    return GPIO.input(pin)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    for relay in config["relays"]:
        client.subscribe(f'home-auto/sprinklers/zones/{relay["id"]}/state')


def on_message(client, userdata, msg):
    print(f'Topic {msg.topic} Message: {msg.payload.decode()}')

    for relay in config["relays"]:
        relay_id = msg.topic.split("/")[-2]
        topic_message = msg.payload.decode()

        if f'{relay_id}' in relay["id"]:
            gpio_pin = relay["pin"]

            if topic_message == 'off':
                GPIO.output(gpio_pin, GPIO.LOW)
                print(f'gpio pi {gpio_pin} state set to \'off\'')
                client.publish(f'home-auto/sprinklers/zones/{relay["id"]}/status', get_gpio_state(pin=gpio_pin))
                if get_gpio_state(pin=gpio_pin) == 0:
                    client.publish(f'home-auto/sprinklers/zones/{relay["id"]}/status', 'off')

            if topic_message == 'on':
                GPIO.output(gpio_pin, GPIO.HIGH)
                print(f'gpio pi {gpio_pin} state set to \'on\'')
                if get_gpio_state(pin=gpio_pin) == 1:
                    client.publish(f'home-auto/sprinklers/zones/{relay["id"]}/status', 'on')



def connect_mqtt():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for relay in config['relays']:
        GPIO.setup(relay['pin'], GPIO.OUT)
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


