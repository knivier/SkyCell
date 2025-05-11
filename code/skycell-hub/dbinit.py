import sqlite3

conn = sqlite3.connect(r'skycell-hub\data\telemetry.db')
c = conn.cursor()

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
        barometric REAL
    )
''')

conn.commit()
conn.close()
print("Database initialized.")
# This script initializes a SQLite database for telemetry data.