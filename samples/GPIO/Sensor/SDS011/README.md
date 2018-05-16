# SDS011 Air Quality Sensor (UART接続) サンプル
SDS011 Air Quality Sensor モジュール SDS011 を SCORER で利用するためのサンプル

## 接続
Raspberry Pi3 と SDS011 付属のUSB シリアル変換モジュールを使って接続する

## SCORER シリアルポートを利用する場合
下記のコマンド実効が必要
```
pip install --user pyserial
```

## ライブラリ

1. サンプルを実行してみる
```bash
cd ~/scorer-sdk-python/samples/GPIO/Sensor/SDS011/examples
sample.py
```

## サンプル実行方法
1. サンプルへのアクセス
http://xxx.xxx.xxx.xxx:20002/samples/GPIO/Sensor/SDS011/
2. 操作方法
ブラウザ画面に SDS011 で取得した値が表示される<br>
![実行した画面]()

## ライブラリサンプル
SDS011 をシンプルに利用したサンプルコード
```python:sample.py
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/libs")

import time
import SDS011
import json

sds011 = SDS011.SDS011('/dev/ttyUSB0')

sds011.begin()

result = sds011.read()
#sds011.sleep()
#sds011.wakeup()

sds011.end()

#status = result['status']
#pm25 = result['pm25']
#pm10 = result['pm10']

print(json.dumps(result))
#result_json = {'status':status,'pm25':pm25,'pm10':pm10}
#print(json.dumps(result_json))
```

1. SDS011(port) <br> UART ポートを設定して初期化
2. begin() <br>
3. read() <br> PM2.5,PM10 を取得する
4. end() <br>
5. wakeup() <br>
6. sleep() <br>
