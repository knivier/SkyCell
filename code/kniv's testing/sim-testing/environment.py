# File: environment.py
import random

class Environment:
    def __init__(self):
        self.wind_speed = 5.0
        self.wind_direction = 0.0
        self.temperature = -20.0
        self.pressure = 700.0
        self.rf_interference = 0.1
        self.solar_radiation = 0.8

    def update(self):
        self.wind_speed += random.uniform(-0.2, 0.2)
        self.wind_direction = (self.wind_direction + random.uniform(-1, 1)) % 360
        self.temperature += random.uniform(-0.5, 0.5)
        self.pressure += random.uniform(-0.3, 0.3)
        self.rf_interference = min(max(self.rf_interference + random.uniform(-0.02, 0.02), 0), 1)
        self.solar_radiation = min(max(self.solar_radiation + random.uniform(-0.05, 0.05), 0), 1)

    def get_conditions(self):
        return {
            "wind_speed": round(self.wind_speed, 2),
            "wind_direction": round(self.wind_direction, 2),
            "temperature": round(self.temperature, 2),
            "pressure": round(self.pressure, 2),
            "rf_interference": round(self.rf_interference, 2),
            "solar_radiation": round(self.solar_radiation, 2)
        }
