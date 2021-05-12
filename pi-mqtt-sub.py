import random

from paho.mqtt import client as mqtt_client



broker = "192.168.0.191"
port = 1883
topic = "hackdays/test"
client_id = 'pi-mqtt-1'
# username = 'emqx'
# password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # client = mqtt_client.Client(client_id)
    client = mqtt_client.Client()
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.mqtt_topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def main():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    main()