from gps import GPSReader
import time

def get_gps_data():
    # Initialize GPS reader - adjust port as needed
    gps = GPSReader(port='/dev/ttyACM0', baudrate=9600)
    
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

# Example usage
if __name__ == "__main__":
    while True:
        try:
            gps_data = get_gps_data()
            if gps_data:
                print(f"Latitude: {gps_data['latitude']}")
                print(f"Longitude: {gps_data['longitude']}")
                print(f"Altitude: {gps_data['altitude']}")
                print(f"Has GPS Fix: {gps_data['has_fix']}")
            else:
                print("No GPS data available")
            time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping GPS reader...")
            break