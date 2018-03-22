
import serial
import re
import time

class HR168(object):
    """HR168"""
    MAX_DISTANCE = 50.0
    result = {'distance':"-1",'time':"0"}

    def __init__(self, port, **kwargs):
        """Initialize"""
        self.serial = serial.Serial(port=port,
                        baudrate=19200,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=10)

    def get_distance(self):
        self.result = {'distance':"-1",'time':"0"}
        self.serial.write("D")
        time.sleep(1.0)
        if self.serial.in_waiting > 0 :
            line=self.serial.readline()
            print(line)

            if line.startswith("D:Er"):
                return {'distance': "ERROR"}

            v = line[2:8]
            self.result = {'distance':float(v),'time':int(v[4])}
            """ ['D', '', '1.189', "", '0047', '', ''] """

        return self.result

    def start_ranging(self):
        """start_ranging"""
        self.serial.write("O")
        self.serial.readline()

    def stop_ranging(self):
        """stop_ranging"""
        self.serial.write("C")
        self.serial.readline()
        self.serial.close()
