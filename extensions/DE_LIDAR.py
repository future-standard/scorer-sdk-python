
import serial
"""
DE-LIDAR TF01 10m
DE-LIDAR TF02 22m
DE-LIDAR TF03 12m
"""

class DE_LIDAR(object):
    """DE_LIDAR"""
    DE_LIDAR_TF01 = 1000
    DE_LIDAR_TF02 = 2200
    DE_LIDAR_TF03 = 1200
    result = {'distance':0,'strength':0,'sig':0,'time':0}

    def __init__(self, port, **kwargs):
        """Initialize"""
        self.serial = serial.Serial(port='/dev/ttyAMA0',
                        baudrate=115200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=10)

    def get_distance(self):
        distance = 0
        strength = 0
        sig = 0
        time = 0
        if self.serial.in_waiting > 0 :
            v = int(self.serial.read().encode('hex'),16)
            if v == 0x59 :
                v = int(self.serial.read().encode('hex'),16)
                if v == 0x59 :
                    dst_l = int(self.serial.read().encode('hex'),16)
                    dst_h = int(self.serial.read().encode('hex'),16)
                    signal_l = int(self.serial.read().encode('hex'),16)
                    signal_h = int(self.serial.read().encode('hex'),16)
                    sig = int(self.serial.read().encode('hex'),16)
                    time = int(self.serial.read().encode('hex'),16)

                    # Distance is shown by HEX,eg.1000 cm = 03 E8(HEX)
                    # print "dst h {0} l {1}".format(hex(dst_h),hex(dst_l))

                    check = (dst_l + dst_h + signal_l + signal_h + sig + time + 0x59 + 0x59)
                    v = int(self.serial.read().encode('hex'),16)
                    if v == (check & 0xff) :
                        """ Calculate distance """
                        distance = (dst_l + (dst_h * 256))
                        strength = (signal_l + (signal_h * 256))

                    self.result = {'distance':distance,'strength':strength,'sig':sig,'time':time}
        return self.result

    def start_ranging(self):
        """start_ranging"""

    def stop_ranging(self):
        self.serial.close()

    def is_sig_success(self):
        return (self.result['sig'] == 0x07) or (self.result['sig'] == 0x08)
