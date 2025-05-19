from meshtastic.serial_interface import SerialInterface

def on_receive(packet, interface):
    print("📩 Received packet:")
    print(packet)

iface = SerialInterface()
iface.onReceive = on_receive

print("Receiver running... Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    iface.close()
    print("Receiver stopped.")
