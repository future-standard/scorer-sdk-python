import sys,os
sys.path.append(os.pardir+"/libs")

import HR168

# Create a HR168 object
hr168 = HR168.HR168('/dev/ttyUSB0')

# Start ranging
hr168.start_ranging()

result = hr168.get_distance()
print ("distance %f m" % (result['distance']))

hr168.stop_ranging()
