# VL53L1X 赤外線測距センサ (I2C接続) サンプル
赤外線測距センサ VL53L1X を SCORER で利用するためのサンプル

## 接続
| &nbsp; | Raspberry Pi3 | VL53L1X |
|:-----------:|:------------:|:------------:|
| SDA | 3 | SDA |
| SCK | 5 | SCK |
| 3.3v | 1 | 3.3V |
| GND | 9 | GND |

## ライブラリ

1. サンプルを実行してみる
```bash
cd ~/scorer-sdk-python/samples/Sensor/VL53L1X/examples
sample.py
```

## サンプル実行方法
1. サンプルへのアクセス
http://xxx.xxx.xxx.xxx:20002/samples/Sensor/VL53L1X/
2. 操作方法
ブラウザ画面に VL53L1X で取得した距離が表示される<br>
![実行した画面]()
