import paho.mqtt.client as mqtt  # import client library

client = mqtt.Client("Anton")  # создание клиента
client.connect("127.0.0.1", 9001, 60)  # подключение к брокеру

client.publish("house/light", "ON")
