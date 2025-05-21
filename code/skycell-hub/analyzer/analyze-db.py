import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

DB_FILE = r'skycell-hub\data\telemetry.db'

def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM telemetry", conn, parse_dates=["timestamp"])
    conn.close()
    df['timestamp'] = pd.to_datetime(df['timestamp'])  # Ensure proper datetime parsing
    return df

def summary(df):
    print("\n--- Data Summary ---")
    print(df.describe())
    print(f"\nTotal Entries: {len(df)}")
    print(f"Date Range: {df['timestamp'].min()} to {df['timestamp'].max()}")

def filter_by_time(df):
    start = input("Enter start datetime (YYYY-MM-DD HH:MM:SS): ")
    end = input("Enter end datetime (YYYY-MM-DD HH:MM:SS): ")
    try:
        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)
        filtered = df[(df['timestamp'] >= start_dt) & (df['timestamp'] <= end_dt)]
        print(f"\nFiltered to {len(filtered)} rows.")
        return filtered
    except Exception as e:
        print("Invalid datetime format.")
        return df

def plot_column(df):
    col = input("Enter column to plot (altitude, temperature, signal_strength, bandwidth, barometric): ")
    if col not in df.columns:
        print("Invalid column.")
        return
    df.plot(x='timestamp', y=col, title=f"{col.title()} Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel(col.title())
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def export_csv(df):
    filename = input("Enter filename to export as CSV (e.g., output.csv): ")
    df.to_csv(filename, index=False)
    print(f"Exported to {filename}")

def main():
    print("== SkyCell Telemetry Analyzer ==")
    df = load_data()

    while True:
        print("\nOptions:")
        print("1. View summary")
        print("2. Filter by time range")
        print("3. Plot a column")
        print("4. Export current data to CSV")
        print("5. Reload data")
        print("6. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            summary(df)
        elif choice == '2':
            df = filter_by_time(df)
        elif choice == '3':
            plot_column(df)
        elif choice == '4':
            export_csv(df)
        elif choice == '5':
            df = load_data()
            print("Data reloaded.")
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

if __name__ == '__main__':
    main()
