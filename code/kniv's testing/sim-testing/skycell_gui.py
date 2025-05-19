# File: skycell_gui.py

import json
import os
import subprocess
import threading
from PyQt6 import QtWidgets, QtCore

DATA_PATH = "code/skycell-hub/data/balloon_state.json"
SIMULATION_SCRIPT = r"code\kniv's testing\sim-testing\balloon_sim.py"

class BalloonGUI(QtWidgets.QWidget):
    def __init__(self, data_path):
        super().__init__()
        self.data_path = data_path
        self.setWindowTitle("SkyCell Telemetry Dashboard")
        self.setGeometry(400, 200, 400, 300)
        self.init_ui()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(1000)  # Update GUI every second

        self.simulation_thread = threading.Thread(target=self.start_simulation)
        self.simulation_thread.daemon = True
        self.simulation_thread.start()

    def init_ui(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.labels = {}

        fields = [
            "altitude", "latitude", "longitude", "temperature",
            "signal_strength", "bandwidth", "barometric",
            "battery", "interference", "last_updated"
        ]

        for field in fields:
            label = QtWidgets.QLabel(f"{field}: N/A")
            self.layout.addWidget(label)
            self.labels[field] = label

        self.setLayout(self.layout)

    def refresh_data(self):
        if not os.path.exists(self.data_path):
            return

        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)

            for key, label in self.labels.items():
                value = data.get(key, "N/A")
                label.setText(f"{key.capitalize().replace('_', ' ')}: {value}")
        except Exception as e:
            print(f"Error reading data: {e}")

    def start_simulation(self):
        subprocess.run(["python", SIMULATION_SCRIPT])

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    gui = BalloonGUI(DATA_PATH)
    gui.show()
    app.exec()
