// will simulate the sensor board by sending dummy uart datat
// format: 0,0,0,0
#include <Arduino.h>
#include <HardwareSerial.h>
HardwareSerial Serial1(1);
void setup() {
  Serial.begin(115200);
  
}
void loop() {
  // send dummy data
  Serial.print("0,0,0,0");
  Serial.flush();
  delay(1000);
  
}