#!/usr/bin/env python3
"""
GPS NMEA Data Reader
Reads GPS NMEA sentences from /dev/ttyS2 and parses them using pynmea2
"""

import serial
import pynmea2
import time
import sys
from datetime import datetime

class GPSReader:
    def __init__(self, port='/dev/ttyS2', baudrate=9600, timeout=1):
        """
        Initialize GPS reader
        
        Args:
            port: Serial port path (default: /dev/ttyS2)
            baudrate: Baud rate (default: 9600, common for GPS modules)
            timeout: Read timeout in seconds
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        
    def connect(self):
        """Connect to the GPS module"""
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            print(f"Connected to {self.port} at {self.baudrate} baud")
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from GPS module"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Disconnected from GPS module")
    
    def read_nmea_sentence(self):
        """Read a single NMEA sentence from the GPS module"""
        if not self.ser or not self.ser.is_open:
            return None
        
        try:
            line = self.ser.readline().decode('ascii', errors='ignore').strip()
            if line.startswith('$'):
                return line
        except Exception as e:
            print(f"Error reading from gps serial port (function read_nmea_sentence): {e}")
        return None
    
    def parse_gps_data(self, nmea_sentence):
        """Parse NMEA sentence and extract GPS data"""
        try:
            msg = pynmea2.parse(nmea_sentence)
            return msg
        except pynmea2.ParseError as e:
            print(f"Parse error: {e}")
            return None
    
    def get_position_data(self, msg):
        """Extract position data from parsed NMEA message"""
        data = {}
        
        # Handle different NMEA sentence types
        if hasattr(msg, 'latitude') and msg.latitude is not None:
            data['latitude'] = float(msg.latitude)
            data['lat_dir'] = msg.lat_dir
            
        if hasattr(msg, 'longitude') and msg.longitude is not None:
            data['longitude'] = float(msg.longitude)
            data['lon_dir'] = msg.lon_dir
            
        if hasattr(msg, 'altitude') and msg.altitude is not None:
            data['altitude'] = float(msg.altitude)
            data['altitude_units'] = msg.altitude_units
            
        if hasattr(msg, 'timestamp') and msg.timestamp is not None:
            data['timestamp'] = msg.timestamp
            
        if hasattr(msg, 'datestamp') and msg.datestamp is not None:
            data['datestamp'] = msg.datestamp
            
        if hasattr(msg, 'gps_qual') and msg.gps_qual is not None:
            data['gps_quality'] = int(msg.gps_qual)
            
        if hasattr(msg, 'num_sats') and msg.num_sats is not None:
            data['satellites'] = int(msg.num_sats)
            
        if hasattr(msg, 'horizontal_dil') and msg.horizontal_dil is not None:
            data['hdop'] = float(msg.horizontal_dil)
            
        if hasattr(msg, 'spd_over_grnd') and msg.spd_over_grnd is not None:
            data['speed_knots'] = float(msg.spd_over_grnd)
            
        if hasattr(msg, 'true_course') and msg.true_course is not None:
            data['course'] = float(msg.true_course)
            
        return data
    
    def run_continuous(self, callback=None, display_raw=False):
        """
        Continuously read and parse GPS data
        
        Args:
            callback: Optional function to call with parsed data
            display_raw: Whether to display raw NMEA sentences
        """
        if not self.connect():
            return
        
        print("Reading GPS data... Press Ctrl+C to stop")
        
        try:
            while True:
                nmea_sentence = self.read_nmea_sentence()
                
                if nmea_sentence:
                    if display_raw:
                        print(f"Raw: {nmea_sentence}")
                    
                    parsed_msg = self.parse_gps_data(nmea_sentence)
                    
                    if parsed_msg:
                        position_data = self.get_position_data(parsed_msg)
                        
                        if position_data:
                            if callback:
                                callback(position_data, parsed_msg)
                            else:
                                self.display_position_data(position_data, parsed_msg)
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
        except Exception as e:
            print("\nError during GPS reading:", e)
        finally:
            self.disconnect()
    
    def display_position_data(self, data, msg):
        """Display formatted GPS position data"""
        print(f"\n--- GPS Data ({datetime.now().strftime('%H:%M:%S')}) ---")
        print(f"Message Type: {msg.__class__.__name__}")
        
        if 'latitude' in data and 'longitude' in data:
            lat_sign = -1 if data.get('lat_dir') == 'S' else 1
            lon_sign = -1 if data.get('lon_dir') == 'W' else 1
            
            print(f"Position: {data['latitude'] * lat_sign:.6f}°, {data['longitude'] * lon_sign:.6f}°")
            print(f"Lat/Lon: {data['latitude']:.6f}°{data.get('lat_dir', '')}, {data['longitude']:.6f}°{data.get('lon_dir', '')}")
        
        if 'altitude' in data:
            print(f"Altitude: {data['altitude']}{data.get('altitude_units', '')}")
        
        if 'satellites' in data:
            print(f"Satellites: {data['satellites']}")
        
        if 'gps_quality' in data:
            quality_desc = {0: "Invalid", 1: "GPS fix", 2: "DGPS fix", 3: "PPS fix", 
                           4: "RTK", 5: "Float RTK", 6: "Estimated", 8: "Manual"}
            print(f"GPS Quality: {quality_desc.get(data['gps_quality'], 'Unknown')} ({data['gps_quality']})")
        
        if 'hdop' in data:
            print(f"HDOP: {data['hdop']}")
        
        if 'speed_knots' in data:
            speed_kmh = data['speed_knots'] * 1.852
            print(f"Speed: {data['speed_knots']:.1f} knots ({speed_kmh:.1f} km/h)")
        
        if 'course' in data:
            print(f"Course: {data['course']:.1f}°")
        
        if 'timestamp' in data:
            print(f"Time: {data['timestamp']}")


def custom_data_handler(position_data, parsed_msg):
    """
    Custom handler function example
    You can modify this to process GPS data as needed
    """
    if 'latitude' in position_data and 'longitude' in position_data:
        lat = position_data['latitude']
        lon = position_data['longitude']
        
        # Apply hemisphere corrections
        if position_data.get('lat_dir') == 'S':
            lat = -lat
        if position_data.get('lon_dir') == 'W':
            lon = -lon
        
        print(f"Location: {lat:.6f}, {lon:.6f}")
        
        # Add your custom processing here
        # For example: log to database, send to web service, etc.


if __name__ == "__main__":
    # Create GPS reader instance
    gps = GPSReader(port='/dev/ttyACM0', baudrate=9600) # /dev/ttyS2 /dev/ttyACM0
    
    # Option 1: Run with default display
    print("Starting GPS reader with default display...")
    gps.run_continuous()
    
    # Option 2: Run with custom callback (uncomment to use)
    # print("Starting GPS reader with custom handler...")
    # gps.run_continuous(callback=custom_data_handler)
    
    # Option 3: Run with raw NMEA display (uncomment to use)
    # print("Starting GPS reader with raw NMEA display...")
    # gps.run_continuous(display_raw=True)