import random
import time
import json
import sys

from paho.mqtt import client as mqtt_client

broker = 'vernemq.rdbox.aio101.intec.lan'
port = 32022
topic = "v1/devices/me/"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        hertlate = random.uniform(70.0, 75.0)
        msg = {"temperature": 36.5, "heartbeat": int(hertlate)}
        result = client.publish(topic, json.dumps(msg))
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    broker = sys.argv[1]
    port = int(sys.argv[2])
    seq_no = sys.argv[3]
    user = "user{:0>3}".format(seq_no)
    topic = topic + user
    run()