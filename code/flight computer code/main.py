import meshtastic.serial_interface
import time
from telemetry import Telemetry


run = True
meshdevice = "/dev/ttyUSB0"  # Adjust this to your Meshtastic device path 
mesh_node = meshtastic.serial_interface.SerialInterface(meshdevice)
print("\nConnected to Meshtastic interface\n")





def send_message(message):
    mesh_node.sendText(
        text=message,
        wantAck=True,
        wantResponse=True 
        )



while run == True:

    
    telemetry = Telemetry()
    
    
    telemetry.gps_connection_port = "/dev/ttyS2"  # Adjust port as needed

    try:
        telemetry.update_telemetry()
    except Exception as e:
        print(f"Error updating telemetry: {e}")
    
    telemetry_data = telemetry.get_telemetry()
    print("Telemetry data: ", telemetry_data)
    
    try:
        tx_telemetry = str(telemetry_data)
    except Exception as e:
        print(f"Error converting telemetry data to string: {e}")
        tx_telemetry = "Error in telemetry data"
    
    try:
        send_message(tx_telemetry)
        print("Sent telemetry: ", tx_telemetry)
    except Exception as e:
        print(f"Error sending telemetry message attempting reconection: {e}")
        mesh_node.close()
        mesh_node = meshtastic.serial_interface.SerialInterface(meshdevice)
        print("Reconnected to Meshtastic interface\n")

    time.sleep(3)  # Adjust sleep time as needed


mesh_node.close()
exit(0)

