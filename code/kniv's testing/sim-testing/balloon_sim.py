# File: balloon_sim.py

import random
import time
import json
import os
from datetime import datetime
from environment import Environment

BALLOON_STATE_PATH = "code/skycell-hub/data/balloon_state.json"

class Balloon:
    def __init__(self, environment):
        self.env = environment
        self.altitude = 0.0  # Starting on ground
        self.latitude = 42.2808
        self.longitude = -83.7430
        self.battery = 100.0  # percent
        self.signal_strength = 1.0  # 0 to 1
        self.bandwidth = 7  # LoRa bandwidth in kHz
        self.barometric = 1013.25  # sea level pressure in hPa
        self.temperature = 20.0
        self.interference = 0.0
        self.ascent_rate = 5.0  # m/s
        self.descending = False

    def update(self):
        conditions = self.env.get_conditions()

        # Altitude simulation
        if not self.descending:
            self.altitude += self.ascent_rate + random.uniform(-0.5, 0.5)
            if self.altitude >= 100000:
                self.descending = True
        else:
            self.altitude -= self.ascent_rate + random.uniform(-0.5, 0.5)
            if self.altitude <= 0:
                self.altitude = 0
                self.descending = False

        # Simulate signal degradation
        self.signal_strength = max(0.0, 1.0 - conditions['rf_interference'] - random.uniform(0.0, 0.1))

        # Simulate GPS drift
        self.latitude += random.uniform(-0.0002, 0.0002)
        self.longitude += random.uniform(-0.0002, 0.0002)

        # Update environment variables
        self.temperature = conditions['temperature'] - (0.0065 * self.altitude / 1000)  # lapse rate
        self.barometric = conditions['pressure'] - (0.12 * self.altitude / 1000)
        self.interference = conditions['rf_interference']

        # Battery drain with solar effect
        solar = conditions['solar_radiation']
        drain = 0.05 - (solar * 0.02)
        self.battery = max(0.0, self.battery - drain)

    def write_state(self):
        state = {
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

        os.makedirs(os.path.dirname(BALLOON_STATE_PATH), exist_ok=True)
        with open(BALLOON_STATE_PATH, 'w') as f:
            json.dump(state, f, indent=2)

        print(json.dumps(state, indent=2))

if __name__ == '__main__':
    env = Environment()
    balloon = Balloon(env)

    while True:
        balloon.update()
        balloon.write_state()
        time.sleep(1)  # Update every second
