from gps import GPSReader
import os
import serial
import pynmea2
import time

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
            return int(temp_str) / 1000.0  # Convert to °C
    except FileNotFoundError:
        return None
def get_battery_voltage():
    # Placeholder for battery voltage reading logic
    # Implement this function to read the actual battery voltage
    return 3.7  # Example value in volts



class Telemetry:
    def __init__(self, gps_connection_port="/dev/ttyS2"):
        self.cpu_temp = None
        self.battery_voltage = None
        self.gps_connection_port = gps_connection_port
        self.gps_data = None
    
    def get_telemetry(self):
        print(self.gps_data)
        return f"telemetry_packet: cput({self.cpu_temp}) batv({self.battery_voltage}) gps(lat({self.gps_data['latitude']}) long({self.gps_data['longitude']}) alt({self.gps_data['altitude']}) hasfix({self.gps_data['has_fix']}))"
           
        
        


    def get_gps_data(self):
    
        # Initialize GPS reader - adjust port as needed
        gps = GPSReader(port=self.gps_connection_port, baudrate=9600)

        if not gps.connect():
            return None

        try:
            # Read until we get valid data or timeout
            start_time = time.time()
            while (time.time() - start_time) < 5:  # 5 second timeout
                nmea = gps.read_nmea_sentence()
                if nmea:
                    msg = gps.parse_gps_data(nmea)
                    if msg:
                        data = gps.get_position_data(msg)
                        if data:
                            result = {
                                'latitude': None,
                                'longitude': None,
                                'altitude': None,
                                'has_fix': False
                            }

                            # Extract position data
                            if 'latitude' in data and 'longitude' in data:
                                result['latitude'] = data['latitude']  
                                result['longitude'] = data['longitude']  
                                print("debug longitude:", result['longitude'])
                            if 'altitude' in data:
                                result['altitude'] = data['altitude']

                            # Check GPS fix
                            if 'gps_quality' in data:
                                result['has_fix'] = data['gps_quality'] > 0

                            return result
                time.sleep(0.1)

            return None

        finally:
            gps.disconnect()

    def update_telemetry(self):
        self.cpu_temp = get_cpu_temp()
        self.gps_data = self.get_gps_data()  # Placeholder for GPS coordinates

        #self.battery_voltage = get
        #self.battery_voltage = get_battery_voltage()  # Implement this function if needed
        #self.battery_percentage = get_battery_percentage()  # Implement this function if needed
    