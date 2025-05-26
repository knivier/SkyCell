# gui.py
import sys
from PyQt6 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from balloon import Balloon
from environment import Environment
import time

class BalloonPlot(FigureCanvas):
    def __init__(self, balloon):
        self.balloon = balloon
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setFixedWidth(600)
        self.path_lat = []
        self.path_long = []
        self.ax.set_title("Balloon Flight Path")
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")

    def update_plot(self):
        self.path_lat.append(self.balloon.latitude)
        self.path_long.append(self.balloon.longitude)
        self.ax.clear()
        self.ax.plot(self.path_long, self.path_lat, color='skyblue', linestyle='-', marker='o', markersize=3)
        self.ax.set_title("Balloon Flight Path")
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")
        margin = 0.005
        if len(self.path_long) > 1:
            self.ax.set_xlim(min(self.path_long)-margin, max(self.path_long)+margin)
            self.ax.set_ylim(min(self.path_lat)-margin, max(self.path_lat)+margin)
        self.ax.grid(True)
        self.fig.tight_layout()
        self.draw()

class AltitudePlot(FigureCanvas):
    def __init__(self, balloon):
        self.balloon = balloon
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.setFixedSize(400, 500)
        self.max_display_alt = 100  # Initial Y-axis max height
        self.ax.set_title("Balloon Altitude")
        self.ax.set_ylabel("Altitude (m)")

    def update_plot(self):
        self.ax.clear()
        self.ax.set_title("Balloon Altitude")
        self.ax.set_xlim(0, 1)
        if self.balloon.altitude > self.max_display_alt * 0.9:
            self.max_display_alt = min(self.max_display_alt * 1.5, 36576)  # 120,000 ft in meters
        self.ax.set_ylim(0, self.max_display_alt)
        self.ax.plot([0.5], [self.balloon.altitude], marker='^', color='red', markersize=14)
        self.ax.text(0.5, self.balloon.altitude + 0.02 * self.max_display_alt, f"{int(self.balloon.altitude)} m", ha='center')
        self.ax.get_xaxis().set_visible(False)
        self.ax.set_ylabel("Altitude (m)")
        self.ax.grid(True)
        self.fig.tight_layout()
        self.draw()

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.env = Environment()
        self.balloon = Balloon(self.env)
        self.start_time = time.perf_counter()

        self.setWindowTitle("SkyCell Balloon Simulator")
        self.resize(1200, 750)

        self.latlong_plot = BalloonPlot(self.balloon)
        self.altitude_plot = AltitudePlot(self.balloon)

        self.info_labels = {}
        info_layout = QtWidgets.QVBoxLayout()
        info_title = QtWidgets.QLabel("<b>Telemetry Data</b>")
        info_layout.addWidget(info_title)
        for key in ['altitude', 'latitude', 'longitude', 'temperature', 'signal_strength', 'battery', 'interference']:
            label = QtWidgets.QLabel()
            label.setStyleSheet("font-size: 14px;")
            self.info_labels[key] = label
            info_layout.addWidget(label)

        self.time_label = QtWidgets.QLabel("Time since launch: 0.0s")
        self.time_label.setStyleSheet("font-size: 14px; margin-top: 10px;")
        info_layout.addWidget(self.time_label)

        plots_layout = QtWidgets.QHBoxLayout()
        plots_layout.addWidget(self.latlong_plot)
        plots_layout.addWidget(self.altitude_plot)
        plots_layout.addLayout(info_layout)

        self.setLayout(plots_layout)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(int(1000 / 1000.0))  # Allow float-like high FPS simulation

    def update_gui(self):
        current_time = time.perf_counter()
        elapsed = current_time - self.start_time

        self.balloon.update()
        self.latlong_plot.update_plot()
        self.altitude_plot.update_plot()

        self.info_labels['altitude'].setText(f"Altitude: {self.balloon.altitude:.2f} m")
        self.info_labels['latitude'].setText(f"Latitude: {self.balloon.latitude:.6f}")
        self.info_labels['longitude'].setText(f"Longitude: {self.balloon.longitude:.6f}")
        self.info_labels['temperature'].setText(f"Temperature: {self.balloon.temperature:.2f} °C")
        self.info_labels['signal_strength'].setText(f"Signal: {self.balloon.signal_strength:.2f}")
        self.info_labels['battery'].setText(f"Battery: {self.balloon.battery:.2f} %")
        self.info_labels['interference'].setText(f"Interference: {self.balloon.interference:.2f}")

        self.time_label.setText(f"Time since launch: {elapsed:.1f}s")

def run():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run()
