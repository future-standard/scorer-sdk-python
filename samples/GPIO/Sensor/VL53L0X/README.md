# VL53L0X 赤外線測距センサ (I2C接続) サンプル
赤外線測距センサ VL53L0X を SCORER で利用するためのサンプル

## 接続
| &nbsp; | Raspberry Pi3 | VL53L0X |
|:-----------:|:------------:|:------------:|
| SDA | 3 | 9 |
| SCK | 5 | 10 |


## ライブラリ

1.  [VL53L0X_rasp_python](https://github.com/johnbryanmoore/VL53L0X_rasp_python) (MITライセンス)をクローンする
```bash
cd ~/scorer-sdk-python/samples/Sensor/VL53L0X/libs
git clone https://github.com/johnbryanmoore/VL53L0X_rasp_python.git
cd VL53L0X_rasp_python
make
```
2. サンプルを実行してみる
```bash
cd ~/scorer-sdk-python/samples/Sensor/VL53L0X/examples
sample.py
```

## サンプル実行方法
1. サンプルへのアクセス
http://xxx.xxx.xxx.xxx:20002/samples/Sensor/VL53L0X/
2. 操作方法
ブラウザ画面に VL53L0X で取得した距離が表示される<br>
![実行した画面](https://raw.githubusercontent.com/tfuru/tf-scorer-sensor/master/VL53L0X/resources/screencapture.png?token=ADwbnqeOloi_C-SOyvFjMx9hm5Byufykks5Z0goOwA%3D%3D)

