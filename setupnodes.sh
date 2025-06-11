#!/bin/bash
# check if nodes have txco
meshtastic --set lora.use_preset false --set location_reporting_enabled false --set telemetry_enabled false --set hop_limit 3 --ch-index 0 --ch-set psk "" --set lora.bandwidth 31 --set lora.spread_factor 12 --set lora.coding_rate 8 