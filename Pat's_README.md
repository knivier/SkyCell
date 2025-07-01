## This is pretty much only for the hackclub ysws database.
my initial research and planning involvement (briefly)
Back in around april we started working on this project back then most of it was planning so back then i did most of the hardware research id say. Our goal from the start was to enable long range comunications in the event where the internet and cell service has gone
out for example after a natural disaster or a big accident this payload would be able to connect the people affected by the natural disaster to first responders or to anyone they need to reach. Our original plan to do this was to use an sdr setup so that we could 
have a cellular tower something like 3G where cellphones themselves could connect to the balloon with the need of no extra radio devices on the ground and then you could even launch a fleet of balloons and have them relay even longer distances. But unfortunately we realised
pretty early on that even if we managed to pull it off with a 400usd budget it would take much longer than 1 months develop and get working so instead we opted for meshtastic. Which is also great because it can greatly diminish the cost of the balloons themselves but ultimately 
in a future mission a cell tower would be better. I did a bunch of research on meshtastic, how it worked, ranges, how the network works, protocol, speeds etc and realised it would work pretty great and you can get a meshtastic node for as low as 20 usd if you're good at finding
deals.

With that decided i also suggested we add an sdr and log raw rf data to later analyze the interference, noise, noise floor, and other factors at different altitudes and different frequencies so that in an imaginary (prob) future mission where we do use an sdr setup and have a cellular tower
we know what frequencies will work best and if anything changes at altitude.

What i built:
- I was in charge of most of the hardware and unfortunately of all the hardware that went on the final flight. (Knivier worked on some sensors for additional info but unfortunately the sensors seemed to have died)
- that means I setup the flight computer, coated it (along with other components to water proof them), and programmed it (radxa rock 5c lite sbc) for which you can find the code and even the systemctl files under the code/flight computer folder
- wrote the ground station receiving code (the ground station was a meshtastic node and a computer) which you can find in the ground station code
- setup the gps and wrote code for it
- wrote the telemetry code and setup both meshtastic nodes + helped setup the 3rd one for testing
- setup and tested the power system (even though it ended up just being a usb power pack which only lasted 40mins due to the buck converter failing, which i would have known if i had an adjustable power supply :( )
- took care of the sdr code, testing all components antenna, tweaking values to be right, cables etc and later started writing code to visualise the data and calibrate it
- packing it all into a styrofoam box to insulate it all
- making sure we are within the weight limit. we were VERY close if not a bit overweight if i recall correctly.
- making sure everything was logged onto the sd card on the balloon side and the ground station also logged correctly.
