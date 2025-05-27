

# File: balloon.py
import random
from datetime import datetime

class Balloon:
    def __init__(self, environment):
        self.env = environment
        self.altitude = 0.0
        self.latitude = 42.2808
        self.longitude = -83.7430
        self.battery = 100.0
        self.signal_strength = 1.0
        self.bandwidth = 7
        self.barometric = 1013.25
        self.temperature = 20.0
        self.interference = 0.0
        self.ascent_rate = 5.0
        self.descending = False
        self.path = [(self.latitude, self.longitude)]

    def update(self):
        conditions = self.env.get_conditions()

        if not self.descending:
            self.altitude += self.ascent_rate + random.uniform(-0.5, 0.5)
            if self.altitude >= 100000:
                self.descending = True
        else:
            self.altitude -= self.ascent_rate + random.uniform(-0.5, 0.5)
            if self.altitude <= 0:
                self.altitude = 0
                self.descending = False

        self.signal_strength = max(0.0, 1.0 - conditions['rf_interference'] - random.uniform(0.0, 0.1))

        lat_drift = random.uniform(-0.0002, 0.0002)
        lon_drift = random.uniform(-0.0002, 0.0002)
        self.latitude += lat_drift
        self.longitude += lon_drift
        self.path.append((self.latitude, self.longitude))

        self.temperature = conditions['temperature'] - (0.0065 * self.altitude / 1000)
        self.barometric = conditions['pressure'] - (0.12 * self.altitude / 1000)
        self.interference = conditions['rf_interference']

        solar = conditions['solar_radiation']
        drain = 0.05 - (solar * 0.02)
        self.battery = max(0.0, self.battery - drain)

    def get_state(self):
        return {
            "altitude": round(self.altitude, 2),
            "latitude": round(self.latitude, 6),
            "longitude": round(self.longitude, 6),
            "temperature": round(self.temperature, 2),
            "signal_strength": round(self.signal_strength, 2),
            "bandwidth": self.bandwidth,
            "barometric": round(self.barometric, 2),
            "last_updated": datetime.utcnow().isoformat() + "Z",
            "battery": round(self.battery, 2),
            "interference": round(self.interference, 2)
        }

