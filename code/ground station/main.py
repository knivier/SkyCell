import struct

# Example: received raw payload (as bytes)
# Replace this with your actual received data
received_payload = b'\x2b\x00\x00\x00\x46\x46\x9b\xff\x92\x41\x05\x00\x00\x00\x26\x91\x08'


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
