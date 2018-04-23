import serial

class SDS011(object):
    """SDS011"""
    SLEEPCMD = [
        0xAA,	# head
    	0xB4,	# command id
    	0x06,	# data byte 1
    	0x01,	# data byte 2 (set mode)
    	0x00,	# data byte 3 (sleep)
    	0x00,	# data byte 4
    	0x00,	# data byte 5
    	0x00,	# data byte 6
    	0x00,	# data byte 7
    	0x00,	# data byte 8
    	0x00,	# data byte 9
    	0x00,	# data byte 10
    	0x00,	# data byte 11
    	0x00,	# data byte 12
    	0x00,	# data byte 13
    	0xFF,	# data byte 14 (device id byte 1)
    	0xFF,	# data byte 15 (device id byte 2)
    	0x05,	# checksum
    	0xAB	# tail
    ]

    def __init__(self, port, **kwargs):
        """Initialize"""
        self.serial = serial.Serial(port=port,
                        baudrate=9600,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=10)
    def begin(self):
        """begin"""

    def end(self):
        """end"""
        self.serial.close()

    def sleep(self):
        """sleep"""
        for cmd in self.SLEEPCMD:
            self.serial.write(cmd)
        while self.serial.inWaiting():
            print self.serial.readline()

    def wakeup(self):
        """wakeup"""
        self.serial.write(0x01)

    def read(self):
        """read"""
        result = {"status":False,"pm25":-1,"pm10":-1}
        success = False
        checksum_ok = False
        checksum_is = 0
        pm25_serial = 0
        pm10_serial = 0
        while 1:
            v = int(self.serial.read().encode('hex'),16) # 0
            #print("0 {0}".format(v))
            if(v != 170):
                break
            else:
                v = int(self.serial.read().encode('hex'),16) # 1
                #print("1 {0}".format(v))
                if(v != 192):
                    break
                else:
                    v = int(self.serial.read().encode('hex'),16) # 2
                    #print("2 {0}".format(v))
                    pm25_serial = v
                    checksum_is = v

                    v = int(self.serial.read().encode('hex'),16) # 3
                    #print("3 {0}".format(v))
                    pm25_serial += (v << 8)
                    checksum_is += v;

                    v = int(self.serial.read().encode('hex'),16) # 4
                    #print("4 {0}".format(v))
                    pm10_serial = v
                    checksum_is += v;

                    v = int(self.serial.read().encode('hex'),16) # 5
                    #print("5 {0}".format(v))
                    pm10_serial += (v << 8)
                    checksum_is += v;

                    v = int(self.serial.read().encode('hex'),16) # 6
                    #print("6 {0}".format(v))
                    checksum_is += v;

                    v = int(self.serial.read().encode('hex'),16) # 7
                    #print("7 {0}".format(v))
                    checksum_is += v;

                    v = int(self.serial.read().encode('hex'),16) # 8
                    #print("8 {0}".format(v))
                    c = (checksum_is % 256)
                    #print("checksum_is {0} v {1}".format(c,v))
                    if (v != c):
                        break
                    else:
                        checksum_ok = True
                        v = int(self.serial.read().encode('hex'),16) # 9
                        #print("9 {0}".format(v))
                        if (v != 171):
                            break
                        else:
                            success = True
                            break
                #if(v != 192):
            #if(v != 170):
        #while ---
        #print("pm10_serial {0} pm25_serial {1}".format(pm10_serial,pm25_serial))
        if checksum_ok == True and success == True :
            pm10 = pm10_serial/10.0
            pm25 = pm25_serial/10.0
            result = {"status":True,"pm25":pm25,"pm10":pm10}

        return result
