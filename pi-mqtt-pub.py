#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import yaml
# import time
# import RPi.GPIO as GPIO

config = yaml.full_load(open('./config.yaml'))

mqtt_broker = config['mqtt_configs']['broker01']['host']
mqtt_port = config['mqtt_configs']['broker01']['port']
mqtt_topic = config['mqtt_configs']['broker01']['status_topic']

gpio_pin = config['gpio_configs']['pin']
# client_id = 'pi-mqtt'
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(channel, GPIO.OUT)

def get_gpio_state(pin=None):
    GPIO.input(pin)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    msg = get_gpio_state(pin=gpio_pin)
    result = client.publish(mqtt_topic, msg)
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{mqtt_topic}`")
    else:
        print(f"Failed to send message to topic {mqtt_topic}")

def connect_mqtt():
    # def on_connect(client, userdata, flags, rc):
    #     if rc == 0:
    #         print("Connected to MQTT Broker!")
    #     else:
    #         print("Failed to connect, return code %d\n", rc)
    # client = mqtt_client.Client()
    # # client = mqtt_client.Client(client_id)
    # # client.username_pw_set(username, password)
    # client.on_connect = on_connect
    # client.connect(mqtt_broker, mqtt_port)
    # return client
    client = mqtt.Client()
    client.on_connect = on_connect
    # client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()


# def publish(client):
#     msg_count = 0
#     while True:
#         time.sleep(1)
#         msg = "hello"
#         result = client.publish(mqtt_topic, msg)
#         # result: [0, 1]
#         status = result[0]
#         if status == 0:
#             print(f"Send `{msg}` to topic `{mqtt_topic}`")
#         else:
#             print(f"Failed to send message to topic {mqtt_topic}")
#         msg_count += 1


def main():
    # client = connect_mqtt()
    # client.loop_start()
    # publish(client)
    connect_mqtt()


if __name__ == '__main__':
    main()
