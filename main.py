import pymongo
from pymongo import MongoClient
import random
import time
import numpy as np
from sklearn.linear_model import LinearRegression

client = MongoClient('mongodb://mongodb:27017/')
db = client['sensores-nest']
collection = db['sensores']

sensors = [
    {
        "sensor_id": 1,
        "sensor_name": "Sensor de clima",
        "data": []
    },
    {
        "sensor_id": 2,
        "sensor_name": "Sensor meteorológico",
        "data": []
    },
    {
        "sensor_id": 3,
        "sensor_name": "Sensor Ambiental",
        "data": []
    }
]

for sensor in sensors:
    collection.insert_one(sensor)

def generate_sensor_data(sensor):
    timestamp = int(time.time())

    if sensor["sensor_name"] == "Sensor de clima":
        X = np.array([[timestamp]])
        temperature_model = LinearRegression()
        temperature_model.fit(X, np.array([random.uniform(20, 30)]))  # Simula temperatura entre 20°C y 30°C
        temperature = temperature_model.predict(X)[0]

        humidity_model = LinearRegression()
        humidity_model.fit(X, np.array([random.uniform(40, 60)]))  # Simula humedad entre 40% y 60%
        humidity = humidity_model.predict(X)[0]

        data = {
            'timestamp': timestamp,
            'temperature': temperature,
            'humidity': humidity
        }

    elif sensor["sensor_name"] == "Sensor meteorológico":
        data = {
            'timestamp': timestamp,
            'pressure': random.uniform(1010, 1020),
            'wind_speed': random.uniform(1, 10)
        }

    elif sensor["sensor_name"] == "Sensor Ambiental":
        data = {
            'timestamp': timestamp,
            'noise_level': random.uniform(30, 50),
            'air_quality': random.choice(["Buena", "Moderada", "Mala"])
        }

    collection.update_one(
        {"sensor_id": sensor["sensor_id"]},
        {"$push": {"data": data}}
    )

# Ejecuta la generación de datos cada 5 segundos
while True:
    for sensor in sensors:
        generate_sensor_data(sensor)
    print("Datos generados y actualizados en MongoDB.")
    time.sleep(5)  # Cambio el tiempo de espera a 5 segundos
