import time
import struct

class BMP180:
    def __init__(self, i2c, addr=0x77):
        self.i2c = i2c
        self.addr = addr
        self._read_calibration()

    def _read_calibration(self):
        def readS16(reg):
            d = self.i2c.readfrom_mem(self.addr, reg, 2)
            return struct.unpack('>h', d)[0]

        def readU16(reg):
            d = self.i2c.readfrom_mem(self.addr, reg, 2)
            return struct.unpack('>H', d)[0]

        self.AC1 = readS16(0xAA)
        self.AC2 = readS16(0xAC)
        self.AC3 = readS16(0xAE)
        self.AC4 = readU16(0xB0)
        self.AC5 = readU16(0xB2)
        self.AC6 = readU16(0xB4)
        self.B1  = readS16(0xB6)
        self.B2  = readS16(0xB8)
        self.MB  = readS16(0xBA)
        self.MC  = readS16(0xBC)
        self.MD  = readS16(0xBE)

    def read_temperature(self):
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x2E')
        time.sleep_ms(5)
        d = self.i2c.readfrom_mem(self.addr, 0xF6, 2)
        UT = struct.unpack('>H', d)[0]

        X1 = ((UT - self.AC6) * self.AC5) >> 15
        X2 = (self.MC << 11) // (X1 + self.MD)
        B5 = X1 + X2
        temp = ((B5 + 8) >> 4) / 10
        self.B5 = B5
        return temp

    def read_pressure(self):
        self.i2c.writeto_mem(self.addr, 0xF4, b'\x34')
        time.sleep_ms(8)
        d = self.i2c.readfrom_mem(self.addr, 0xF6, 3)
        UP = ((d[0] << 16) + (d[1] << 8) + d[2]) >> 8

        B6 = self.B5 - 4000
        X1 = (self.B2 * (B6 * B6 >> 12)) >> 11
        X2 = (self.AC2 * B6) >> 11
        X3 = X1 + X2
        B3 = (((self.AC1 * 4 + X3) << 0) + 2) >> 2
        X1 = (self.AC3 * B6) >> 13
        X2 = (self.B1 * (B6 * B6 >> 12)) >> 16
        X3 = ((X1 + X2) + 2) >> 2
        B4 = (self.AC4 * (X3 + 32768)) >> 15
        B7 = (UP - B3) * 50000
        if B7 < 0x80000000:
            p = (B7 << 1) // B4
        else:
            p = (B7 // B4) << 1
        X1 = (p >> 8) * (p >> 8)
        X1 = (X1 * 3038) >> 16
        X2 = (-7357 * p) >> 16
        return p + ((X1 + X2 + 3791) >> 4)

    def read_altitude(self, sea_level_pressure=101325.0):
        p = self.read_pressure()
        return 44330.0 * (1.0 - pow(p / sea_level_pressure, 0.1903))

