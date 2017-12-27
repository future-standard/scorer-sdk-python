import sys,os
sys.path.append(os.pardir)

from libs import BME280

bme280 = BME280.BME280(BME280.BME280_ADDRESS)
bme280.setup()
bme280.readData()
print "pressure : %7.2f hPa" % (bme280.getPressure()/100)
print "temp : %-6.2f ℃" % (bme280.getTemperature())
print "hum : %6.2f ％" % (bme280.getHum())
