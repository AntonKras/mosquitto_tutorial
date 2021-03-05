import paho.mqtt.client as mqtt
import time
import json


def create_message(number):
    dict_msg = {
        "my_field": number
    }
    return dict_msg


client_1 = mqtt.Client("Anton")  # создание клиента
client_1.connect("127.0.0.1", 9001, 60)  # подключение к брокеру
client_1.loop_start()
time.sleep(4)

client_1.subscribe("sensors")

i = 0
while True:
    for number in range(0, 10):
        msg = json.dumps(create_message(number))
        client_1.publish("sensors", msg)
    for number in range(10, 0, -1):
        msg = json.dumps(create_message(number))
        client_1.publish("sensors", msg)
