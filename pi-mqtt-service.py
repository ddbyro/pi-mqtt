#!/usr/bin/env python3.7
import paho.mqtt.client as mqtt
import yaml
import time
# from RPiSim.GPIO import GPIO
import RPi.GPIO as GPIO

config = yaml.full_load(open('./config.yaml'))

mqtt_broker = config['broker_configs']['host']
mqtt_port = config['broker_configs']['port']
# mqtt_status_topic = config['relays'][0]['status_topic']
# mqtt_set_topic = config['relays'][0]['set_topic']
# gpio_pin = config['relays'][0]['pin']

# gpio_pin = ""
# for relay in config['relays']:


def set_gpio_state(pin=None, state=None):
    GPIO.setup(pin, state)



def get_gpio_state(pin=None):
    return GPIO.input(pin)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    # Subscribing to receive RPC requests
    # client.subscribe(mqtt_set_topic)
    #print(f'Topic {msg.topic} Message: {msg.payload.decode()}')
    # for relay in config['relays']:
    #     print(client.subscribe(relay['set_topic']))
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

            if topic_message == 'on':
                GPIO.output(gpio_pin, GPIO.HIGH)
                print(f'gpio pi {gpio_pin} state set to \'on\'')
                client.publish(f'home-auto/sprinklers/zones/{relay["id"]}/status', get_gpio_state(pin=gpio_pin))


        # GPIO.output(gpio_pin, GPIO.LOW)

    # for relay in config["relays"]:
    #     print(client.subscribe(f'home-auto/zone{relay["id"]}'))

        # for relay in config['relays']:
        #     client.subscribe(f"{relay['name']}/set")
        #     gpio_pin = relay['pin']
        #
        #
        #     if msg.payload.decode() == '0':
        #         print(f'gpio pi {gpio_pin} state set to \'off\'')
        #         print(msg.payload.decode())
        #         # set_gpio_state(pin=gpio_pin, state=GPIO.LOW)
        #         # GPIO.setup(gpio_pin, GPIO.OUT)
        #         GPIO.output(gpio_pin, GPIO.LOW)
        #
        #     if msg.payload.decode() == '1':
        #         print(f'gpio pi {gpio_pin} state set to \'on\'')
        #         # set_gpio_state(pin=gpio_pin, state=GPIO.HIGH)
        #         # GPIO.setup(gpio_pin, GPIO.OUT)
        #         GPIO.output(gpio_pin, GPIO.HIGH)






def connect_mqtt():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    for relay in config['relays']:
        GPIO.setup(relay['pin'], GPIO.OUT)
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    # client.on_subscribe = on_subscribe
    # client.on_publish = on_publish
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()


def main():
    try:
        connect_mqtt()
    except KeyboardInterrupt:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
    #
    # GPIO.setwarnings(False)
    # GPIO.setmode(GPIO.BCM)
    # gpio_pin = int(config['relays']['pin'])
    # set_gpio_state(pin=gpio_pin, state=GPIO.LOW)
    # for relay in config['relays']:
    #
    #     print(get_gpio_state(gpio_pin))

