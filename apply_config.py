import meshtastic
from meshtastic.serial_interface import SerialInterface
import json

iface = SerialInterface()

with open("node-config.json", "r") as f:
    config = json.load(f)

iface.localNode.writeConfig(config)
iface.close()

print("Config applied.")
'''
import yaml
import json

with open("node-config.yaml", "r") as f:
    yaml_data = yaml.safe_load(f)

with open("node-config.json", "w") as f:
    json.dump(yaml_data["config"], f, indent=2)
'''