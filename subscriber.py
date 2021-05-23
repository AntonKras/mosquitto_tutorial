import paho.mqtt.client as mqtt
import time
from influxdb import InfluxDBClient
from queue import Queue

INFLUXDB_ADDRESS = '127.0.0.1'
INFLUXDB_USER = 'telegraf'
INFLUXDB_PASSWORD = 'telegraf'
INFLUXDB_DATABASE = 'sensors'

influxdb_client = InfluxDBClient(INFLUXDB_ADDRESS, 8086, INFLUXDB_USER, INFLUXDB_PASSWORD, database=INFLUXDB_DATABASE)


def send_sensor_data_to_influxdb(number: float or int) -> None:
    """
    создает JSON для отправки в influxdb
    """
    json_body = [
        {
            "measurement": "temperature",
            "tags": {
                "host": "paris_1",
            },
            "fields": {
                "value": float(number)
            }
        }
    ]
    influxdb_client.write_points(json_body)
    return None


def init_influxdb_database() -> None:
    """
    создает базу данных, если ее не существует
    """
    databases = influxdb_client.get_list_database()
    if len(list(filter(lambda x: x['name'] == INFLUXDB_DATABASE, databases))) == 0:
        influxdb_client.create_database(INFLUXDB_DATABASE)
    influxdb_client.switch_database(INFLUXDB_DATABASE)
    return None


def on_message(client, userdata, message):
    data = str(message.payload.decode("utf-8"))

    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    q.put(data)


q = Queue()
time.sleep(25)
init_influxdb_database()
client_2 = mqtt.Client("Anton_2")
client_2.on_message = on_message
client_2.connect("127.0.0.1", 1883, 60)  # подключение к брокеру
client_2.loop_start()
print('Подключен')
client_2.subscribe('sensors/temperature')
while True:
    time.sleep(4)
    client_2.on_message = on_message
    while not q.empty():
        message = q.get()
        send_sensor_data_to_influxdb(message)
        if message is None:
            continue
        print("received from queue", message)
    time.sleep(4)  # wait
