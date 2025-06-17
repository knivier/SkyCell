from gps import GPSReader
import os
import serial
import pynmea2
import time
import struct

# reminder to self: pressure, humidity, temp, altitude
external_sensors_port = "/dev/tty_tty8"  # Adjust this to your external sensors port

def get_external_sensors():
    # Placeholder for external sensors reading logic
    # Implement this function to read actual sensor data
    # start new serial connection to the external sensors

    default_error_return = {
        'pressure': 37,  # Example value in hPa
        'humidity': 37,     # Example value in %
        'temperature': 37,  # Example value in °C
        'altitude': 37     # Example value in meters
    }

    try:
        ser = serial.Serial(external_sensors_port, baudrate=115200, timeout=1)
        
    except Exception as e:
        print(f"Error opening serial port: {e}")
        try:
            ser.close()
        except Exception as e:
            print(f"Error closing serial port: {e}")
        return default_error_return

    try:
        line = ser.readline().decode('ascii', errors='ignore').strip()
        
    except Exception as e:
        print(f"Error reading from external gps serial: {e}")
        try:
            ser.close()
        except Exception as e:
            print(f"Error closing serial port: {e}")
        return default_error_return
    
    print("External sensors data:", line)

    # format: "pressure,humidity,temperature,altitude"
    try:
        pressure, humidity, temperature, altitude = map(int, line.split(','))
        return_data = {
            'pressure': pressure,  # in hPa
            'humidity': humidity,  # in %
            'temperature': temperature,  # in °C
            'altitude': altitude  # in meters
        }
        print("sensor data:", return_data)
        try:
            ser.close()
        except Exception as e:
            print(f"Error closing serial port: {e}")
        return  return_data
    except Exception as e:
        print(f"Error parsing external sensors data: {e}")
        
    
    try:
        ser.close()
    except Exception as e:
        print(f"Error closing serial port: {e}")
    return default_error_return
    


def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
            return int(temp_str) / 1000.0  # Convert to °C
    except FileNotFoundError:
        return 37
    
def get_battery_voltage():
    # Placeholder for battery voltage reading logic
    # Implement this function to read the actual battery voltage
    return 3.7  # Example value in volts

def get_uptime():
    try:
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.read().split()[0])
            return uptime_seconds
    except Exception as e:
        print(f"Error reading uptime: {e}")
        return 0.0  # Return 0 if unable to read uptime

class Telemetry:
    def __init__(self, gps_connection_port="/dev/ttyS2"):
        self.cpu_temp = 0
        self.battery_voltage = 0
        self.gps_connection_port = gps_connection_port
        self.gps_data = {
            'latitude': 0.0,
            'longitude': 0.0,
            'altitude': 0.0,
            'has_fix': False
        }
        self.battery_voltage = 0.0
        self.uptime = 0.0
        self.external_sensor_data = {
        'pressure': 0,  # Example value in hPa
        'humidity': 0,     # Example value in %
        'temperature': 0,  # Example value in °C
        'altitude': 0     # Example value in meters
    }
    
    def get_telemetry(self, packet_number=0):
        

        # print log of all readings
        try:
            print(f"Cpu Temp: {self.cpu_temp} °C, Battery Voltage: {self.battery_voltage} V, "
                f"GPS Latitude: {self.gps_data['latitude']}°N, "
                f"GPS Longitude: {self.gps_data['longitude']}°E, "
                f"GPS Altitude: {self.gps_data['altitude']} m, "
                f"GPS Fix: {self.gps_data['has_fix']}, Uptime: {self.uptime} seconds, Packet Number: {packet_number}, sensor data: {self.external_sensor_data}")
        except Exception as e:
            print(f"Error printing telemetry data: {e}")
        



        # transform data to integers for packing
        cpu_temp_int = max(-128, min(127, int(self.cpu_temp)))
        batv_int = max(0, min(65535, int(self.battery_voltage * 1000)))
        lat_int = max(-2147483648, min(2147483647, int(self.gps_data['latitude'] * 1e5)))
        long_int = max(-2147483648, min(2147483647, int(self.gps_data['longitude'] * 1e5)))
        alt_int = max(0, min(65535, int(self.gps_data['altitude'])))
        has_fix_int = 1 if self.gps_data['has_fix'] else 0
        uptime_int = max(0, min(65535, int(self.uptime)))
        packet_number_int = max(0, min(127, int(packet_number)))

        sensor_pressure_int = max(-128, min(127, int(self.external_sensor_data['pressure'])))
        sensor_humidity_int = max(-128, min(127, int(self.external_sensor_data['humidity'])))
        sensor_temperature_int = max(-128, min(127, int(self.external_sensor_data['temperature'])))
        sensor_altitude_int = max(-128, min(127, int(self.external_sensor_data['altitude'])))

        # Pack into bytes (big endian, signed for lat/long)
        packed = struct.pack(
            '>bHiiHbHbbbbb',  # format: > for big-endian, H for unsigned short (2 bytes), i for signed int (4 bytes), b for signed char (1 byte)
            cpu_temp_int, # 1bytes
            batv_int, # 2bytes
            lat_int, # 4bytes
            long_int, # 4bytes
            alt_int, # 2bytes
            has_fix_int, # 1byte
            uptime_int, # 2bytes
            packet_number_int,  # 1 bytes total: 17 bytes

            sensor_pressure_int,  # 1 byte
            sensor_humidity_int,  # 1 byte
            sensor_temperature_int,  # 1 byte
            sensor_altitude_int   # 1 byte total: 21 bytes
        )

        # Convert to hex string for transmission
        telemetry_hex_string = packed.hex()
        
        return telemetry_hex_string
           
        
        


    def get_gps_data(self):
    
        # Initialize GPS reader - adjust port as needed
        gps = GPSReader(port=self.gps_connection_port, baudrate=9600) 

        if not gps.connect():
            return {
                                'latitude': 0.0,
                                'longitude': 0.0,
                                'altitude': 0.0,
                                'has_fix': False
                            }

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
                                'latitude': 0.0,
                                'longitude': 0.0,
                                'altitude': 0.0,
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

            return {
                                'latitude': 0.0,
                                'longitude': 0.0,
                                'altitude': 0.0,
                                'has_fix': False
                            }

        finally:
            gps.disconnect()

    def update_telemetry(self):
        self.cpu_temp = get_cpu_temp()
        self.gps_data = self.get_gps_data()  # Placeholder for GPS coordinates
        self.uptime = get_uptime()
        self.external_sensor_data = get_external_sensors()  # Get external sensors data
        self.battery_voltage = get_battery_voltage()
        #self.battery_voltage = get_battery_voltage()  # Implement this function if needed
        #self.battery_percentage = get_battery_percentage()  # Implement this function if needed
    