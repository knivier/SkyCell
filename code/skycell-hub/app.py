# This primary app connects the flask app to the telemetry database and the balloon state JSON file.
# It serves the dashboard and provides an API endpoint for the latest telemetry data.
from flask import Flask, render_template, jsonify
import json
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DATA_FILE = r'skycell-hub\data\balloon_state.json'
DB_FILE = r'skycell-hub\data\telemetry.db'

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

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/data')
def api_data():
    data = read_balloon_data()
    if data:
        data['last_updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_to_db(data)
        return jsonify(data)
    else:
        return jsonify({"error": "No data found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
