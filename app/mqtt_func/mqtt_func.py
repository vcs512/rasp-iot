import random
import time
from paho.mqtt import client as mqtt_client


# broker = 'localhost'
broker = 'broker.hivemq.com'
port = 1883
topic = "sel0373/vigiSEL/Motion"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def publish(client, msg):
    # msg = f"messages: {msg_count}"
    # msg = 'abriu camera'
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


client = connect_mqtt()
subscribe(client)
publish(client, 'Rasp conectada ao broker MQTT local')


# from app.__init__ import mqtt

# def mqtt_publish(topic, message):
#     # mqtt.publish('Motion', 'abriu camera')
#     mqtt.publish(topic, message)