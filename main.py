import pymongo
from pymongo import MongoClient
import random
import time
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

client = MongoClient('mongodb://mongodb:27017/')
db = client['sensores-nest']
collection = db['sensors']

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
    # Obtén la fecha y hora actual del sistema
    current_time = datetime.now()

    if sensor["sensor_name"] == "Sensor de clima":
        X = np.array([[current_time.timestamp()]])
        temperature_model = LinearRegression()
        temperature_model.fit(X, np.array([random.uniform(20, 30)]))  # Simula temperatura entre 20°C y 30°C
        temperature = temperature_model.predict(X)[0]

        humidity_model = LinearRegression()
        humidity_model.fit(X, np.array([random.uniform(40, 60)]))  # Simula humedad entre 40% y 60%
        humidity = humidity_model.predict(X)[0]

        data = {
            'timestamp': current_time.timestamp() * 1000,
            'temperature': temperature,
            'humidity': humidity
        }

    elif sensor["sensor_name"] == "Sensor meteorológico":
        X = np.array([[current_time.timestamp()]])
        pressure_model = LinearRegression()
        pressure_model.fit(X, np.array([random.uniform(1010, 1020)]))
        pressure = pressure_model.predict(X)[0]

        wind_speed_model = LinearRegression()
        wind_speed_model.fit(X, np.array([random.uniform(1, 10)]))
        wind_speed = wind_speed_model.predict(X)[0]
        data = {
            'timestamp': current_time.timestamp() * 1000,
            'pressure': pressure,
            'wind_speed': wind_speed
        }

    elif sensor["sensor_name"] == "Sensor Ambiental":
        X = np.array([[current_time.timestamp()]])
        noise_level_model = LinearRegression()
        noise_level_model.fit(X, np.array([random.uniform(30, 50)]))
        noise_level = noise_level_model.predict(X)[0]

        data = {
            'timestamp': current_time.timestamp() * 1000,
            'noise_level': noise_level,
            'air_quality': random.choice(["Buena", "Moderada", "Mala"])
        }

    collection.update_one(
        {"sensor_id": sensor["sensor_id"]},
        {"$push": {"data": data}}
    )

while True:
    for sensor in sensors:
        generate_sensor_data(sensor)
    print("Datos generados y actualizados en MongoDB.")
    time.sleep(5)
