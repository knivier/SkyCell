import sqlite3
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
from datetime import datetime

DB_PATH = r"skycell-hub\data\telemetry.db"

def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, altitude, temperature, signal_strength, bandwidth,
               barometric, battery, interference
        FROM telemetry
        ORDER BY id DESC
        LIMIT 100
    """)
    rows = c.fetchall()
    conn.close()
    return rows[::-1]  # Return in chronological order

def animate(i):
    rows = fetch_data()
    if not rows:
        return

    timestamps = [datetime.fromisoformat(row[0]) for row in rows]
    altitude = [row[1] for row in rows]
    temperature = [row[2] for row in rows]
    signal_strength = [row[3] for row in rows]
    bandwidth = [row[4] for row in rows]
    barometric = [row[5] for row in rows]
    battery = [row[6] for row in rows]
    interference = [row[7] for row in rows]

    for ax, data, label in zip(axes.flat, 
                               [altitude, temperature, signal_strength, bandwidth, barometric, battery, interference],
                               ["Altitude (m)", "Temperature (°C)", "Signal Strength (dBm)", 
                                "Bandwidth (Hz)", "Barometric Pressure", "Battery (%)", "RF Interference"]):
        ax.clear()
        ax.plot(timestamps, data, marker='o', linestyle='-', color='skyblue')
        ax.set_title(label)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.grid(True)
        ax.tick_params(axis='x', rotation=45)

    fig.tight_layout()

# Plot Setup
fig, axes = plt.subplots(4, 2, figsize=(16, 12))
axes[3][1].axis('off')  # Hide empty subplot

ani = FuncAnimation(fig, animate, interval=3000)  # Refresh every 3 seconds
plt.suptitle("SkyCell Telemetry Live Dashboard", fontsize=18)
plt.show()
