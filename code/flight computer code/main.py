import meshtastic.serial_interface
import time
from telemetry import Telemetry
import subprocess

run = True
meshdevice = "/dev/ttyUSB0"  # Adjust this to your Meshtastic device path 
mesh_node = meshtastic.serial_interface.SerialInterface(meshdevice)
print("\nConnected to Meshtastic interface\n")





def send_message(message):
    mesh_node.sendData(
        text=message,
        wantAck=False # CHECK REGION SETTINGS AND ADJUST FOR NOSE TOLERANCE
        
        )


packet_number = 0
while run == True:

    packet_number+=1
    if packet_number > 127:
        packet_number = 0
    telemetry = Telemetry()
    
    
    telemetry.gps_connection_port = "/dev/ttyS2"  # Adjust port as needed

    try:
        telemetry.update_telemetry()
    except Exception as e:
        print(f"Error updating telemetry: {e}")
    try:
        telemetry_data = telemetry.get_telemetry(packet_number=packet_number)
    except Exception as e:
        print(f"Error getting telemetry data: {e}")

    
    try:
        
        telemetry_bytes = bytes.fromhex(telemetry_data)
        
        mesh_node.sendData(
            data=telemetry_bytes,  # Send bytes instead of hex string
            wantAck=False,
            portNum=1,
            priority=64
        )
        print(telemetry_bytes)
        print("Raw packed bytes:", [hex(b) for b in telemetry_bytes])
        print("Hex string:", telemetry_data)
        
    except Exception as e:
        print(f"Error sending telemetry message attempting reconection: {e}")
        mesh_node.close()
        mesh_node = meshtastic.serial_interface.SerialInterface(meshdevice)
        print("Reconnected to Meshtastic interface\n")

    time.sleep(15)  # Adjust sleep time as needed


mesh_node.close()
exit(0)

