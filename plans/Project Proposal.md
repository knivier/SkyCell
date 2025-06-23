# **SkyCell: Balloon-Based Disaster Relief Communication System Proposal**

Meddy, Agniva, Sharon, Patricio 

## **1. Introduction**

Natural disasters, such as earthquakes and hurricanes cripple essential infrastructure, such as power and communication systems, leaving many communities and people in devastating conditions without any way to contact help. As reported by FEMA, in the aftermath of the 2017 Hurricane Maria, 95% of cell towers in Puerto Rico had become out of service. Restoring communication systems is crucial for coordinating rescue efforts and allowing survivors to call for help. We propose designing and testing a high-altitude balloon-borne cellular node as a rapid solution to re-establish cellular coverage in disaster zones. Balloons in the stratosphere can provide a wide area–of roughly 900 mile radius—line-of-sight coverage, allowing the payload to act as a cell tower. Major initiatives, such as Alphabet’s Loon project and SoftBank's trials of tethered balloons have validated this approach. Our team plans to build on these concepts while focusing on cost-effectiveness, user friendliness, allowing for affordability, ease of use, and optimal deployment time. The goal is to develop a 1 ft³ <0.75 lb payload that functions as a cell relay at ~100,000 ft altitude for 2–3 hours, allowing for emergency voice/SMS and/or data connectivity to mobile phones on the ground. By using open source cellular technology commercial off-the-shelf components, our system, called Skycell,  will effectively create a rapidly deployed micro cell tower in the sky. It will comply with all regulations and emphasize simplicity and safety.

## **2. Objectives**

* Restore Connectivity Quickly after disasters  
* Fit Small and Light so a single weather balloon can carry it.  
* Operate at 100,000 feet to cover a large area below  
* Use easy-to-build, open-source tools (like GSM and SDR) that our team can handle

## **3. Methodology**

* Phase 1: Design & Simulation  
  * Finalize the system design through simulations and research. Budget calculations, GSM network configuration planning , and parts selection. We will use software tools (e.g. MATLAB or GNURadio simulations) to model the GSM coverage area and capacity. Milestone: Complete schematic of system, get any necessary experimental licenses (e.g. FCC STA or amateur call sign for telemetry). We will also design the ground module that will imitate a phone and test the connection on the ground.  
* Phase 2: Procurement & Bench Testing.   
  * Order all components per the BOM. Once parts arrive, perform bench tests: power on the Raspberry Pi (or similar) and install OpenBTS/YateBTS. Connect the LimeSDR and verify it can transmit a carrier and receive on the chosen band. We will test the BTS software with two test phones on the ground (at low power) to ensure calls/texts work in a small cell configuration. We’ll also measure the current draw of each module to validate the power budget. The RF amplifier will be tested with a signal generator to ensure it provides gain and is stable. Milestone: End-to-end call or SMS made via the system on the bench (with two phones connected through the BTS).  
* Phase 3: Integration  
  * Assembling the components into the payload enclosure. Integrate sensors to log altitude and internal temperature during flight. The payload will be weighed and if overweight, figure out how to save weight. Once integrated, full system tests will be performed by attempting connections. We will verify the broadcasted network appears on phones and that one can place a call between two devices on the network (we’ll use an Asterisk PBX on the Pi or the built-in SIP functionality of OpenBTS to route a call). We’ll measure the RF output with a spectrum analyzer to ensure the filter and amplifier are doing their job . Milestone: Fully integrated payload passes a functional test and is ready for flight.   
* High-Altitude Balloon Launch   
  * Conduct the full balloon launch, following FAA regulations for the launch. On launch day, the system will be powered on a few minutes before release and we’ll verify ground connection one last time. Once launched, the ground team will monitor the telemetry, tracking ascent rate, altitude, and attempt test calls as the balloon ascends. We expect the best connectivity at higher altitudes due to broader line-of-sight. We will also send a message from the balloon to test one-way alerting. We will continue to log data until landing. Milestone: Successful flight with at least one two-way communication achieved between ground unit andpayload. Safe recovery of payload.  
* After the flight, we will analyze logs:   
  * BTS logs (to see how many users connected, signal levels), sensor logs (temperature, battery voltage over time), and any user feedback (voice quality, range). We will prepare results demonstrating the coverage area achieved – e.g. mapping where connections were made. If any part of the system underperformed (battery died early, etc.), we propose solutions (like adding another cell, which we likely budgeted weight for). At this stage, we will also finalize the research report for dissemination. This includes the engineering findings and the potential impact on disaster communications – for instance, extrapolating how multiple such balloon relays could network to cover larger areas or provide mesh backhaul. We will emphasize the success metrics, such as how quickly it was deployed and how many calls it could support, linking back to the overarching goal of improving disaster response. Milestone: Completion of a comprehensive report and, if possible, a demonstration to stakeholders (e.g. a live demo for emergency management officials or at a research expo).

**4. Risk Management**

* **Signal Interference and Legal Compliance**  
   Operating radio systems at high altitudes poses potential risks of interfering with other services. We will fix this by using only approved frequency bands, low transmission power, and RF band-pass filters to minimize disruption.

* **Payload Weight Limitations**  
   The balloon payload must remain under 0.75 lbs. To manage this, we will use lightweight components, measure detailed weight checks, and remove anything nonessential.

* **Power System Failure**  
   Cold stratospheric temperatures can significantly reduce battery performance so we will insulate the battery, use heaters, and use batteries with proven cold-weather reliability, and possibly using solar. Backup systems in our software will allow maximum usage of all communication protocols by prioritizing certain systems as voltage levels continue to drop. 

* **Software Malfunction**  
   The base station software or payload could crash mid-flight. Ground testing will be conducted beforehand as well as automated scripts to restart or reboot the system if a failure is detected. Data from the payload will constantly be transmitted back to the base station.

* **Balloon Drift or Loss of Payload**  
  The payload will include a GPS tracker with a radio link for real-time location updates, as well as mapping the balloon’s path in a 3d  viewer

**7. Expected Outcomes**

* **Demonstration of a Working Airborne GSM Network:**  
   The balloon payload will create a functional connection that connects to standard mobile phones for voice and SMS communication.

* **Successful Communication Testing During Flight:**  
   Real-time voice and SMS tests will be conducted from ground users connected through the balloon’s GSM relay.

* **Wide Area Coverage:**  
   From an altitude of approximately 100,000 feet, we expect signal coverage over a 30–50 km radius.

* **Proof of Concept for Disaster Use:**  
   The results will demonstrate that balloon-based cellular relays are feasible, fast to deploy, and effective in disaster scenarios.

* **Safe Recovery of Payload:**  
   With a parachute and GPS tracker, the payload will be safely recovered for data extraction and potential reuse.

## **8. Conclusion**

* This project presents a practical and innovative solution for restoring emergency communications in disaster-struck regions using a high-altitude balloon. By deploying a lightweight GSM base station into the stratosphere, we aim to reconnect isolated individuals using only the phones they already own. Our approach emphasizes affordability, portability, and ease of deployment. The outcome of this research will validate the potential for such systems to become standard tools in humanitarian response, empowering communities and saving lives when infrastructure fails.

## **9. References**

[https://arxiv.org/abs/2410.13977](https://arxiv.org/abs/2410.13977)

[https://www.theverge.com/2022/9/12/23349291/alphabet-google-project-loon-aalyria-lasers-communication](https://www.theverge.com/2022/9/12/23349291/alphabet-google-project-loon-aalyria-lasers-communication)

[https://www.google.com/search?q=Balloon-Based+Resilient+Communications&oq=Balloon-Based+Resilient+Communications&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg80gEHMTQ2ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8](https://www.google.com/search?q=Balloon-Based+Resilient+Communications&oq=Balloon-Based+Resilient+Communications&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg80gEHMTQ2ajBqN6gCALACAA&sourceid=chrome&ie=UTF-8)

[https://scholar.google.com/scholar?q=Balloon-Based+Resilient+Communications&hl=en&as_sdt=0&as_vis=1&oi=scholart](https://scholar.google.com/scholar?q=Balloon-Based+Resilient+Communications&hl=en&as_sdt=0&as_vis=1&oi=scholart)

[https://ieeexplore.ieee.org/abstract/document/10793319](https://ieeexplore.ieee.org/abstract/document/10793319)

[https://link.springer.com/article/10.1007/s11235-019-00580-w](https://link.springer.com/article/10.1007/s11235-019-00580-w)

[https://www.google.com/search?q=BLoS+communication+relays&oq=BLoS+communication+relays&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDMxMzRqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8](https://www.google.com/search?q=BLoS+communication+relays&oq=BLoS+communication+relays&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDMxMzRqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8)

[https://ieeexplore.ieee.org/abstract/document/9899783](https://ieeexplore.ieee.org/abstract/document/9899783)

**10. Appendices**

* CAD drawings and system schematics.

* Detailed parts list ([BOM](?tab=t.56re0qfyr216)) 

* Calculations and simulations.

**Appendix A: Acronyms**

* **GSM** – Global System for Mobile Communications

* **SDR** – Software-Defined Radio

* **BTS** – Base Transceiver Station

* **HAB** – High-Altitude Balloon

* **EIRP** – Effective Isotropic Radiated Power

* **LTE** – Long-Term Evolution

* **STA** – Special Temporary Authorization (FCC)

**Appendix B: System Software**

* **Raspberry Pi OS / DragonOS** – Operating system for Raspberry Pi

* **OpenBTS / Osmocom** – Open-source GSM base station software

* **Asterisk** – Open-source telephony server (optional)

* **GNURadio** – SDR interface and signal processing toolkit

**Appendix C: Pre-Flight Checklist**

* Battery fully charged and secured

* SDR, amplifier, and Raspberry Pi securely mounted

* GSM software configured and tested

* Antenna tuned and mounted downward

* GPS and LoRa tracker activated

* Balloon and parachute securely attached (to be done by deployment team)

* Weather and airspace conditions verified (to be done by deployment team)  
* Software manual check systems for all sensor calibrations and detections

**Appendix D: Regulatory References**

* **FCC Part 97 & Part 15** – Rules for radio communication and unlicensed devices

* **ITU HAPS Regulations** – Frequency use for high-altitude platforms

* **FAA Balloon Launch Guidelines** – For amateur and research balloon flights (to be done by launch team)
