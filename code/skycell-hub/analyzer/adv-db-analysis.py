import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DB_FILE = r'skycell-hub\data\telemetry.db'

st.set_page_config(page_title="SkyCell Telemetry Dashboard", layout="wide")

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM telemetry", conn)
    conn.close()

    # Ensure timestamp is datetime64[ms], not object or ns
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])  # Drop rows with invalid timestamps
    df['timestamp'] = df['timestamp'].astype('datetime64[ms]')

    # Explicitly convert all numeric columns to float (handles mixed types)
    numeric_cols = ['altitude', 'latitude', 'longitude', 'temperature',
                    'signal_strength', 'bandwidth', 'barometric']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def plot_data(df, y_column):
    fig, ax = plt.subplots()
    ax.plot(df['timestamp'], df[y_column], marker='o', linestyle='-', label=y_column)
    ax.set_xlabel('Timestamp')
    ax.set_ylabel(y_column.title())
    ax.set_title(f"{y_column.title()} Over Time")
    ax.grid(True)
    st.pyplot(fig)

# --- MAIN UI ---
st.title("📡 SkyCell Telemetry Dashboard")

df = load_data()

with st.sidebar:
    st.header("🔎 Filters")
    if not df.empty:
        min_date = df['timestamp'].min().date()
        max_date = df['timestamp'].max().date()
    else:
        min_date = datetime.today().date()
        max_date = datetime.today().date()

    start_date = st.date_input("Start Date", min_date)
    end_date = st.date_input("End Date", max_date)

    columns_to_plot = st.multiselect(
        "Select Data to Plot", 
        options=["altitude", "temperature", "signal_strength", "bandwidth", "barometric"],
        default=["altitude"]
    )

    export = st.button("📤 Export Filtered Data to CSV")

# Filter data
filtered_df = df[(df['timestamp'].dt.date >= start_date) & (df['timestamp'].dt.date <= end_date)]

# Summary
st.subheader("📊 Summary")
st.write(f"Showing {len(filtered_df)} rows from {start_date} to {end_date}")
st.dataframe(filtered_df)

# Stats
st.subheader("📈 Statistics")
st.dataframe(filtered_df.describe())

# Plots
st.subheader("📍 Graphs")
for col in columns_to_plot:
    if col in filtered_df.columns and not filtered_df[col].isnull().all():
        plot_data(filtered_df, col)

# Export
if export:
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, f"telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", "text/csv")
