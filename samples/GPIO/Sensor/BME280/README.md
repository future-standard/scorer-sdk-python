# BME280 温湿度・気圧センサ (I2C 接続) サンプル
温湿度・気圧センサ BME280 を SCORER で利用するためのサンプル

## 接続
| &nbsp; | Raspberry Pi3 | BME280 |
|:-----------:|:------------:|:------------:|
| SDA | 3 | 9 |
| SCK | 5 | 10 |


## BME280 ライブラリサンプル
BME280.pyをシンプルに利用したサンプルコード
```python:sample.py
import sys,os
sys.path.append(os.pardir)

from libs import BME280

bme280 = BME280.BME280(BME280.BME280_ADDRESS)
bme280.setup()
bme280.readData()
print "pressure : %7.2f hPa" % (bme280.getPressure()/100)
print "temp : %-6.2f ℃" % (bme280.getTemperature())
print "hum : %6.2f ％" % (bme280.getHum())

```
