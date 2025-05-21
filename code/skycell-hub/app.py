from flask import Flask, render_template
import json
import sqlite3
from datetime import datetime
import os
import threading
import time

app = Flask(__name__)

DATA_FILE = r'skycell-hub\data\balloon_state.json'
DB_FILE = r'skycell-hub\data\telemetry.db'
LOG_DIR = r'skycell-hub\data\master-logs'

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Generate a unique log filename for this session
log_filename = None
log_path = None
if not os.environ.get('WERKZEUG_RUN_MAIN'):
    # Only set log file in the original process, not the reloader
    start_time = datetime.now()
    log_filename = start_time.strftime('%d%m%Y.%S.%f')[:-3] + '.log'
    log_path = os.path.join(LOG_DIR, log_filename)

def read_balloon_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def log_to_db(data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Ensure the telemetry table exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            altitude REAL,
            latitude REAL,
            longitude REAL,
            temperature REAL,
            signal_strength REAL,
            bandwidth REAL,
            barometric REAL,
            battery REAL,
            interference REAL
        )
    ''')
    c.execute('''
        INSERT INTO telemetry (
            timestamp, altitude, latitude, longitude, temperature,
            signal_strength, bandwidth, barometric, battery, interference
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get("last_updated"),
        data.get("altitude"),
        data.get("latitude"),
        data.get("longitude"),
        data.get("temperature"),
        data.get("signal_strength"),
        data.get("bandwidth"),
        data.get("barometric"),
        data.get("battery"),
        data.get("interference")
    ))
    conn.commit()
    conn.close()

def background_logger():
    while True:
        data = read_balloon_data()
        if data and log_path:
            data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(log_path, 'a') as log_file:
                log_file.write(json.dumps(data) + '\n')
            log_to_db(data)
        time.sleep(1)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    data = read_balloon_data()
    if data:
        data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_to_db(data)
        return data
    return {}

if __name__ == '__main__':
    # Only start the background logging thread in the original process, not the reloader
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        thread = threading.Thread(target=background_logger, daemon=True)
        thread.start()
    app.run(debug=True)
