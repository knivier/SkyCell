# File: environment.py

import random
import threading
import time
from PyQt6 import QtWidgets, QtCore

class Environment:
    def __init__(self):
        self.wind_speed = 5.0  # m/s
        self.wind_direction = 0.0  # degrees
        self.temperature = -20.0  # Celsius
        self.pressure = 700.0  # hPa
        self.rf_interference = 0.1  # 0 to 1
        self.solar_radiation = 0.8  # 0 to 1

    def update(self):
        # Simulate changing environmental conditions
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

class EnvironmentGUI(QtWidgets.QWidget):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.init_ui()
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.refresh)
        self.update_timer.start(1000)

    def init_ui(self):
        self.setWindowTitle("SkyCell Environment Simulator")
        self.layout = QtWidgets.QVBoxLayout()

        self.labels = {}
        for key in self.env.get_conditions().keys():
            label = QtWidgets.QLabel()
            self.layout.addWidget(label)
            self.labels[key] = label

        self.setLayout(self.layout)
        self.setGeometry(300, 300, 300, 200)

    def refresh(self):
        self.env.update()
        conditions = self.env.get_conditions()
        for key, label in self.labels.items():
            label.setText(f"{key.replace('_', ' ').capitalize()}: {conditions[key]}")

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    env = Environment()
    gui = EnvironmentGUI(env)
    gui.show()
    app.exec()
