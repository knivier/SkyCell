# This interprets telemetry.db data and posts it on a GUI
# It will need to be re-ran as telemetry.db is updated
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

DB_PATH = r"skycell-hub\data\telemetry.db"

def fetch_data():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, altitude, latitude, longitude,
               temperature, signal_strength, bandwidth,
               barometric, battery, interference
        FROM telemetry
    """)
    rows = c.fetchall()
    conn.close()
    return rows

def parse_timestamp(ts):
    try:
        return datetime.fromisoformat(ts)
    except ValueError:
        # Fallback in case it's not ISO formatted
        try:
            return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return None

def plot_data(rows):
    timestamps = [parse_timestamp(row[0]) for row in rows if parse_timestamp(row[0])]
    altitude = [row[1] for row in rows]
    temperature = [row[4] for row in rows]
    signal_strength = [row[5] for row in rows]
    bandwidth = [row[6] for row in rows]
    barometric = [row[7] for row in rows]
    battery = [row[8] for row in rows]
    interference = [row[9] for row in rows]

    fig, axs = plt.subplots(4, 2, figsize=(15, 10))
    fig.suptitle("SkyCell Telemetry Analysis", fontsize=16)

    plots = [
        ("Altitude (m)", altitude),
        ("Temperature (°C)", temperature),
        ("Signal Strength (dBm)", signal_strength),
        ("Bandwidth (Hz)", bandwidth),
        ("Barometric Pressure", barometric),
        ("Battery (%)", battery),
        ("RF Interference", interference),
    ]

    for i, (label, data) in enumerate(plots):
        ax = axs[i // 2][i % 2]
        ax.plot(timestamps, data, marker='o', linestyle='-')
        ax.set_title(label)
        ax.grid(True)

    axs[3][1].axis('off')  # hide the unused subplot
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.show()

if __name__ == "__main__":
    data = fetch_data()
    if data:
        plot_data(data)
    else:
        print("No data found in telemetry.db.")
