# DE-LIDAR レーザーライダー (UART接続) サンプル
レーザーライダー DE-LIDAR TF02 を SCORER で利用するためのサンプル

## 接続
| &nbsp; | Raspberry Pi3 | DE-LIDAR |
|:-----------:|:------------:|:------------:|
| TX | 14 | 白(RXD) |
| RX | 15 | 緑(TXD) |

# Raspberry Pi 設定
## /boot/config.txt を編集
Bluetoothを無効にして、シリアルコンソール(ttyAMA0)を有効にする為に  
/boot/config.txt 末尾にこの行を追記する

```
dtoverlay=pi3-miniuart-bt
```

## /boot/cmdline.txt を編集
GPIO で UARTを利用できるようにするために console の記述を削除する

```
console=ttyAMA0,115200
```


## ライブラリ

1. サンプルを実行してみる
```bash
cd ~/scorer-sdk-python/samples/Sensor/DE_LIDAR/examples
sample.py
```

## サンプル実行方法
1. サンプルへのアクセス
http://xxx.xxx.xxx.xxx:20002/samples/Sensor/DE_LIDAR/
2. 操作方法
ブラウザ画面に DE-LIDAR TF02 で取得した距離が表示される<br>
![実行した画面]()

## ライブラリサンプル
DE_LIDAR をシンプルに利用したサンプルコード
```python:sample.py
import sys,os
sys.path.append(os.pardir+"/libs")

import time
import DE_LIDAR

# Create a DE_LIDAR object
tof = DE_LIDAR.DE_LIDAR('/dev/ttyAMA0')

# Start ranging
tof.start_ranging()

distance = 0
while distance != tof.DE_LIDAR_TF02 :
    result = tof.get_distance()
    if tof.is_sig_success() :
        #print result
        distance = result['distance']
        if (distance == tof.DE_LIDAR_TF02) :
            # error distance == DE_LIDAR_TF02[22000]
            print ("error distance.")
        else :
            print ("%d cm" % (distance))
    time.sleep(0.01)

tof.stop_ranging()

```

1. DE_LIDAR(port) <br> UART ポートを設定して初期化
2. get_distance() <br> 距離,シグナル強度,データ信頼性,露光時間 を取得する
3. is_sig_success() <br> データ信頼性の確認 0x07 or 0x08 以外はエラーと判定
4. stop_ranging() <br> UART接続を終了