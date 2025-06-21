# SkyCell

#### The telecommunications solution on a balloon...for broke people alike.

This event was funded by the Apex event where we launched SkyCell on June 21st, 2025. It was the culmination of work from all of our teammates and over two months of planning (not to mention $400 in parts alone funded by Apex and the over $1200 in flight coverage as well).

## The Vision

Hurricanes, tornados, dust storms, and whatever other disasters wreck havoc on communications systems every year, risking lives. Technological dependency for communication has made telecommunication-based systems extremely important, and disasters pose a significant risk to that. 

Our team came up with the idea of SkyCell: A disaster-relief based telecommunications relief package/module that could be a backup incase primary communications systems fail.

## The Goals
1. Receive telemetry data in a JSON format from SkyCell when it is in the air
2. Be able to connect to SkyCell via a LoRA transceiver
3. Send and receive messages using SkyCell through meshtastic software 

## The Execution
### Planning
The initial plans were a basic CAD viewing of what SkyCell could look like along with a basic BOM. We knew we needed LoRA based communications, so we went with ESP-32s due to their relatively affordable prices (specifically, Heltec V3s). Pat also wanted to have SDR logging capabilities, so those components were added as well. We also got our own GPS module because we wanted SkyCell to be largely independent from the main balloon. 

For the main motherboard, we initially wanted to think about using a Raspberry Pi 5. However, it's a known fact that they aren't a great value, and a significantly better deal was a *Radxa Rock 5C*. This board was more efficient and more powerful than the RPi5 while also being cheaper (on amazon that is). 

For power, we initially thought about 4x AA batteries but later went with 8, then 6 for some redundancy. Energizer Li-Ion Ultimate's were chosen as Apex organizers mentioned they were one of the few AAs that supported as low as -40C temperatures. 

For software, we went with a modular design, choosing to implement features slowly as we coded our main board. Built in logging was very important as should SkyCell fail to send messages, we would want to see why. These were written on a local SD card in the R5C. 

We also wanted to implement a camera (you can see remnants of that in `code\kniv's testing`) and created a compression algorithm for that as well that could have sent images over LoRA theoretically. However, this was later cut out in the final planning stages due to the higher expenses.
### Building
The building stage took an additional two months. During this time, parts were coded, assembled, and soldered down. 
#### Launch Night Issues
When testing with battery power (attempting to send/receive messages on battery) and with using a DC current power supply (regulatable), we discovered that the DC buck converter was having issues catching up with 5V, especially when systems like GPS and radios started (see: `project-images\prelaunch_night.jpg`), which caused bootlock and SD card corruption issues. This led to us trying to give as much voltage to the R5C without frying it (we gave up to 5.2v on the DC-DC and supplied 12V at one point), and we also tried large capacitors (up to 10,000µF). We also tried using a custom DC-DC 5V stepdown from another 'Apexer' with no luck. We even used a oscilloscope (that was a new one) to find out voltage patterns and isolate the problem.

In the end, we needed to scratch the idea of having AA batteries and instead chose to have a power bank fitted. This would only give us up to 30min of time, but it was better than having a non-functional project as a whole. 

We also wanted to have some telemetry sensors like a BMP180 for barometric, altitude, and temperature, along with an AHT21 for humidity and more temperature. During the flight though, the BMP180 got fried and when the AHT21 was working, it was already too late to implement a UART based system to connect the Pico to the R5C.
### Launch Time 
The module was launched at around the afternoon and traveled for around two hours. We only received around 3-4 packets of data and were able to connect to the node quite far away (LoRA systems were set up back at the main site while the balloon was launched quite far north). 

## Review

### What parts would we use instead?
For starters, a significantly better DC-DC Buck Converter. The issues would have been fixed if we could give more power to the pi at certain points (ex at startup give the Pi 5V->5.5V->5V) so there was more startup power.

A BME280 would've also been a life saver as it integrates all the sensors we needed (BMP180 + AHT21) into one. 

Finally, although the ESP32s did pick up some transmissions, we only received an estimated <20% of total sent packets. Using a significantly longer antenna along with a GUI-based LoRA system (something like the *# LILYGO T-Deck Plus ESP32-S3 915Mhz LORA-89 SX1262 Ulbox GPS 2.8-inch Display TTGO*) would have likely increased efficiency. 
### What software choices would we do instead?
We should've sent packets more frequently and not tried to do so much in the beginning. In the end, many of our new attempts failed and made it a lot more worse for the stuff that should have been trivial. 

### Did we do what we set out to do?
We never sent out messages on the launch date because the balloon was travelling at 60m/s when we got disconnected (that's over 200kph). However, we did still connect to the node for a minute, and we also received ~mostly~ valid telemetry packets.

SkyCell was never meant to be a full project showcase 100% completed, it was rather a proposal or a proof of concept that it is possible over LoRA

If we were given an extra $200 (bringing the total budget to $600), it's likely that our project would have been a lot more polished, however we're happy that we got live data anyways. 