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
    def __init__(self, cpu_temp, battery_voltage, battery_percentage):
        self.cpu_temp = cpu_temp
        self.battery_voltage = battery_voltage
        


    def to_dict(self):
        return {
            "cput": self.cpu_temp,
            "bv": self.battery_voltage
            
        }

    def update_readings(self):
        self.cpu_temp = get_cpu_temp()
        self.battery_voltage = get
        #self.battery_voltage = get_battery_voltage()  # Implement this function if needed
        #self.battery_percentage = get_battery_percentage()  # Implement this function if needed