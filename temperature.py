import paho.mqtt.client as mqtt
import time
from random import uniform
from influxdb import InfluxDBClient

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
            "measurement": "temperature_value_1",
            "tags": {
                "host": "moscow_1",
            },
            "fields": {
                "value": number
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


def main():
    init_influxdb_database()
    client_1 = mqtt.Client("Anton")
    client_1.connect("127.0.0.1", 1883, 60)  # подключение к брокеру
    client_1.loop_start()
    time.sleep(4)

    while True:
        temperature_value = uniform(-30.0, 30.0)
        send_sensor_data_to_influxdb(temperature_value)


if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()
