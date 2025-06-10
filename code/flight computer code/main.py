import meshtastic.serial_interface
import time
from telemetry import Telemetry
import subprocess

run = True
meshdevice = "/dev/ttyUSB0"  # Adjust this to your Meshtastic device path 
mesh_node = meshtastic.serial_interface.SerialInterface(meshdevice)
print("\nConnected to Meshtastic interface\n")





def send_message(message):
    mesh_node.sendText(
        text=message,
        wantAck=False # CHECK REGION SETTINGS AND ADJUST FOR NOSE TOLERANCE
        
        )


packet_number = 0
while run == True:

    packet_number+=1
    telemetry = Telemetry()
    
    
    telemetry.gps_connection_port = "/dev/ttyS2"  # Adjust port as needed

    try:
        telemetry.update_telemetry()
    except Exception as e:
        print(f"Error updating telemetry: {e}")
    
    telemetry_data = telemetry.get_telemetry()
    print("Telemetry data: ", telemetry_data)
    
    try:
        tx_telemetry = str(telemetry_data + f" paknum{packet_number})")
        print("Telemetry string: ", tx_telemetry)
    except Exception as e:
        print(f"Error converting telemetry data to string: {e}") # TX VIA COMMAND REMEMBER AND CHEC OR CHECK IF ITS NOT BECAUSE OF " AND " OR ' IN JSON DICTIONARY
        tx_telemetry = "Error in telemetry data"
    
    try:
        '''
        # Method 1: Using subprocess.run (recommended)
        cmd = f'meshtastic --sendtext "{tx_telemetry}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("Sent telemetry:", tx_telemetry)
        else:
            print("Error sending telemetry:", result.stderr)'''
        send_message(tx_telemetry)
        #send_message("this is a telemetry message with a lot of numbers and letter : " + str(i))
        # run terminal command meshtastic --sentext "tx_telemetry"

        print("Sent telemetry: ", tx_telemetry)
    except Exception as e:
        print(f"Error sending telemetry message attempting reconection: {e}")
        mesh_node.close()
        mesh_node = meshtastic.serial_interface.SerialInterface(meshdevice)
        print("Reconnected to Meshtastic interface\n")

    time.sleep(15)  # Adjust sleep time as needed


mesh_node.close()
exit(0)

