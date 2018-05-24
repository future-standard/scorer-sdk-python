import sys,os
sys.path.append(os.pardir+"/libs")

import HR168
import time

# Create a HR168 object
hr168 = HR168.HR168('/dev/ttyUSB0')

# Start ranging
hr168.start_ranging()

#time.sleep(3)

result = hr168.get_distance()

if result['distance'] == "ERROR" :
    print("ERROR")
else:    
    print ("distance %03.3f m" % (result['distance']))

hr168.stop_ranging()
