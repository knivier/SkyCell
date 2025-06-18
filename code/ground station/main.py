import struct
import json
import os


import meshtastic.serial_interface
from pubsub import pub
import time
import json
import ast

# Example: received raw payload (as bytes)
# Replace this with your actual received data
#received_payload = b'\x2b\x00\x00\x00\x46\x46\x9b\xff\x92\x41\x05\x00\x00\x00\x26\x91\x08'


# Ensure it matches expected length
def unpack_payload(received_payload, packet):
    if len(received_payload) != 21:
        print("Invalid packet length:", len(received_payload))
    else:
        # Unpack the data
        (
            cpu_temp_int,
            batv_int,
            lat_int,
            long_int,
            alt_int,
            has_fix_int,
            uptime_int,
            packet_number_int,

            sensor_pressure_int,  # 1 byte
            sensor_humidity_int,  # 1 byte
            sensor_temperature_int,  # 1 byte
            sensor_altitude_int   # 1 byte total: 21 bytes
        ) = struct.unpack('>bHiiHbHbbbbb', received_payload)

        # Convert back to usable units
        cpu_temp = cpu_temp_int
        battery_voltage = batv_int / 1000.0
        latitude = lat_int / 1e5
        longitude = long_int / 1e5
        altitude = alt_int
        has_fix = bool(has_fix_int)
        uptime = uptime_int
        packet_number = packet_number_int

        sensor_pressure = sensor_pressure_int
        sensor_humidity = sensor_humidity_int
        sensor_temperature = sensor_temperature_int
        sensor_altitude = sensor_altitude_int

        # Display results
        print("CPU Temp:", cpu_temp, "°C")
        print("Battery Voltage:", battery_voltage, "V")
        print("Latitude:", latitude)
        print("Longitude:", longitude)
        print("Altitude:", altitude, "m")
        print("Has GPS Fix:", has_fix)
        print("Uptime:", uptime, "s")
        print("Packet Number:", packet_number)

        print("Sensor Pressure:", sensor_pressure, "hPa")
        print("Sensor Humidity:", sensor_humidity, "%")
        print("Sensor Temperature:", sensor_temperature, "°C")
        print("Sensor Altitude:", sensor_altitude, "m")

        # radio data
        try:
            rssi = packet.get('rxRssi', 77)
            snr = packet.get('rxSnr', 77)
        except Exception as e:
            rssi = 37
            snr = 37
        
        print("Rssi:", rssi)
        print("SNR:", snr)

        # Print raw packet bytes
        print("Raw packet bytes:", [hex(b) for b in received_payload])

        # convert to json
        telemetry_data = {
            "cpu_temp": cpu_temp,
            "battery_voltage": battery_voltage,
            "latitude": latitude,
            "longitude": longitude,
            "altitude": altitude,
            "has_fix": has_fix,
            "uptime": uptime,
            "packet_number": packet_number,

            "sensor_pressure": sensor_pressure,
            "sensor_humidity": sensor_humidity,
            "sensor_temperature": sensor_temperature,
            "sensor_altitude": sensor_altitude,

            "rssi": rssi,
            "snr": snr
        }


        telemetry_json = json.dumps(telemetry_data, indent=4)
        print("Telemetry JSON:", telemetry_json)
        # Write to telemetry.json
        with open("telemetry.json", 'w') as f:
            f.write(telemetry_json)
            f.flush()
            os.fsync(f.fileno())
        print("Telemetry data written to telemetry.json")
        # Write to telemetry_log.json
        with open("telemetry_log.json", 'a') as f:
            f.write(telemetry_json + '\n')
            f.flush()
            os.fsync(f.fileno())
        print("Telemetry data appended to telemetry_log.json")







interface = meshtastic.serial_interface.SerialInterface("COM13") # PORT
interface.frequency = int(915.5e6)  # Replace with your desired frequency
print("Connected to Meshtastic interface\n")


def onReceive(packet, interface):
    print(f"Raw packet received: {packet}")  # Debug: see the full packet structure
    
        # Extract only the decoded payload from the packet
    if 'decoded' in packet and 'payload' in packet['decoded']:
        payload = packet['decoded']['payload']
        unpack_payload(payload, packet)
    else:
        print("Error: Packet does not contain decoded payload")

# Subscribe to all message types to see what we're actually receiving
pub.subscribe(onReceive, 'meshtastic.receive.text')
# Also try subscribing to telemetry specifically
pub.subscribe(onReceive, 'meshtastic.receive.telemetry')


print("Listening for messages... Press Ctrl+C to stop")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
    interface.close()