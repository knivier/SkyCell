import struct

# Example: received raw payload (as bytes)
# Replace this with your actual received data
received_payload = b'\x2c\x0f\x27\x02\x03\xb3\x17\x2e\xfa\x00\x64\x01\x00\x3c\x05\x3c\x05'

# Ensure it matches expected length
if len(received_payload) != 17:
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
        packet_number_int
    ) = struct.unpack('>bHiiHbHb', received_payload)

    # Convert back to usable units
    cpu_temp = cpu_temp_int
    battery_voltage = batv_int / 1000.0
    latitude = lat_int / 1e5
    longitude = long_int / 1e5
    altitude = alt_int
    has_fix = bool(has_fix_int)
    uptime = uptime_int
    packet_number = packet_number_int

    # Display results
    print("CPU Temp:", cpu_temp, "°C")
    print("Battery Voltage:", battery_voltage, "V")
    print("Latitude:", latitude)
    print("Longitude:", longitude)
    print("Altitude:", altitude, "m")
    print("Has GPS Fix:", has_fix)
    print("Uptime:", uptime, "s")
    print("Packet Number:", packet_number)
