# 50メートルミニサイズレーザー測距モジュール HR168 (UART接続) サンプル
50メートルミニサイズレーザー測距モジュール HR168 を SCORER で利用するためのサンプル

## 接続
Raspberry Pi3 と HR168 付属のUSB シリアル変換モジュールを接続する

## SCORER シリアルポートを利用する場合
下記のコマンド実効が必要
```
pip install --user pyserial
```

## ライブラリ

1. サンプルを実行してみる
```bash
cd ~/scorer-sdk-python/samples/GPIO/Sensor/HR168/examples
sample.py
```

## サンプル実行方法
1. サンプルへのアクセス
http://xxx.xxx.xxx.xxx:20002/samples/GPIO/Sensor/HR168/
2. 操作方法
ブラウザ画面に HR168 で取得した距離が表示される<br>
![実行した画面]()

## ライブラリサンプル
HR168 をシンプルに利用したサンプルコード
```python:sample.py
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__))+"/libs")

import time
import HR168
import json

hr168 = HR168.HR168('/dev/ttyUSB0')

hr168.start_ranging()
distance = -1
status = 'NG'

result = hr168.get_distance()
distance = result['distance']
if(distance != -1){
    status = 'OK'
}

result_json = {'status':status,'distance':distance}
print(json.dumps(result_json))

hr168.stop_ranging()

```

1. HR168(port) <br> UART ポートを設定して初期化
2. get_distance() <br> 距離,時間 を取得する
3. stop_ranging() <br> UART接続を終了
