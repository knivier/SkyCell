import json
import os
import threading
import time
from datetime import datetime
import sqlite3
from flask import Flask, render_template, jsonify

app = Flask(__name__)

DATA_FILE = r'skycell-hub\data\balloon_state.json'
DB_FILE = r'skycell-hub\data\telemetry.db'

# Globals for log file management
log_file_path = None
log_entry_count = 0
log_file_hour = None
import glob

def get_log_file_path():
    now = datetime.now()
    current_hour = now.strftime('%d-%m-%Y-%H')
    log_dir = os.path.join('skycell-hub', 'data')
    pattern = os.path.join(log_dir, f'TELE-SCETUM-{current_hour}-*.log')
    files = glob.glob(pattern)
    if files:
        return files[0]  # Use the first found file for this hour
    else:
        # Create a new file with a unique name for this hour
        filename = f'TELE-SCETUM-{now.strftime("%d-%m-%Y-%H-%M-%S")}.log'
        return os.path.join(log_dir, filename)

def update_log_file():
    global log_file_path, log_file_hour
    now = datetime.now()
    current_hour = now.strftime('%Y-%m-%d-%H')
    if log_file_hour != current_hour or log_file_path is None:
        log_file_hour = current_hour
        log_file_path = get_log_file_path()

def log_to_file(data):
    global log_entry_count
    update_log_file()
    with open(log_file_path, 'a') as f:
        f.write(json.dumps(data) + '\n')
    log_entry_count += 1

def read_balloon_data():
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def log_to_db(data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO telemetry (timestamp, altitude, latitude, longitude, temperature, signal_strength, bandwidth, barometric)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data.get("last_updated"),
        data.get("altitude"),
        data.get("latitude"),
        data.get("longitude"),
        data.get("temperature"),
        data.get("signal_strength"),
        data.get("bandwidth"),
        data.get("barometric")
    ))
    conn.commit()
    conn.close()

def background_updater():
    while True:
        data = read_balloon_data()
        if data:
            data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_to_db(data)
            log_to_file(data)
        time.sleep(1)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    data = read_balloon_data()
    if data:
        data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return jsonify(data)
    else:
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    threading.Thread(target=background_updater, daemon=True).start()
    app.run(debug=True)
