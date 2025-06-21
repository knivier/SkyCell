import time
# Driver for AHT21
class AHT21:
    def __init__(self, i2c, addr=0x38):
        self.i2c = i2c
        self.addr = addr
        self._init_sensor()

    def _init_sensor(self):
        try:
            # Soft reset
            self.i2c.writeto(self.addr, b'\xBA')
            time.sleep(0.02)

            # Init command
            self.i2c.writeto(self.addr, b'\xBE\x08\x00')
            time.sleep(0.01)
        except Exception as e:
            print("AHT21 init error:", e)

    def _trigger_measurement(self):
        self.i2c.writeto(self.addr, b'\xAC\x33\x00')
        time.sleep(0.08)

    def read(self):
        self._trigger_measurement()
        data = self.i2c.readfrom(self.addr, 7)

        if data[0] & 0x80:
            raise Exception("Measurement not complete")

        raw_temp = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        raw_humi = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4))

        humidity = (raw_humi / 1048576.0) * 100
        temperature = (raw_temp / 1048576.0) * 200 - 50

        return round(temperature, 2), round(humidity, 2)

