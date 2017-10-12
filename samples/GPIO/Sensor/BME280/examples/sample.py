import sys,os
sys.path.append(os.pardir)

from libs import BME280

bme280 = BME280.BME280(BME280.BME280_ADDRESS)
