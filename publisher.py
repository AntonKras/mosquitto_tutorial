import paho.mqtt.client as mqtt  # import the client1
import time
from random import uniform

client = mqtt.Client("Anton")  # создание клиента
print("Подключение к брокеру")
client.connect("127.0.0.1", 1883, 60)  # подключение к брокеру
client.loop_start()  # start the loop
print("Отправка сообщений в топик", "sensors")
while True:
    temperature_value = uniform(-30.0, 30.0)    # создание рандомных значений температуры
    client.publish("sensors/temperature", temperature_value)    # отправка значений температуры в топик
    time.sleep(4)