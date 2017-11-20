# DRV8830 I2Cモータードライバー サンプル
デュアルモータードライバー DRV8830 を SCORER で利用するためのサンプル

## 接続
| &nbsp; | Raspberry Pi3 | DRV8830 |
|:-----------:|:------------:|:------------:|
| SDA | 3 | 27 |
| SCK | 5 | 26 |

| &nbsp; | DRV88330 | Motor |
|:-----------:|:------------:|:------------:|
| OUT1 | 2 | 1 |
| OUT2 | 4 | 2 |


![接続した写真](https://raw.githubusercontent.com/tfuru/tf-scorer-actuator/master/Motor/DRV8833/resources/2017-09-27%2018.12.41.jpg?token=ADwbnrZt3wfn2okzK5LiG4voog4evLjFks5Z1hepwA%3D%3D)

## サンプル実行方法
1. サンプルへのアクセス
http://xxx.xxx.xxx.xxx:20002/samples/Actuator/Motor/DRV8833/
2. 操作方法
ブラウザ画面から DRV88330 に接続したモーターを動かす事ができます。<br>
![画面キャプチャ](https://raw.githubusercontent.com/tfuru/tf-scorer-actuator/master/Motor/DRV8833/resources/2017-10-02%2012.55.19.png?token=ADwbnlwP1Z15SwVH1Z4g-l183VHBjF_Kks5Z2vNpwA%3D%3D)

## サンプル内容
javascript からのリクエストで 各モーターを駆動させています。
```javascript:index.js
const $ = function(id){return document.getElementById(id);};
class Index{
  proxy(fn, context){
    return function(){
      return fn.apply(context, arguments);
    };
  }

  getJson(url,op,success,error){
    var param = function(op){
      var queryArray = [];
      Object.keys(op).forEach(function (key) { return queryArray.push(key + '=' + encodeURIComponent(op[key])); });
      return queryArray.join('&');
    };
    var xhr = new XMLHttpRequest();
    xhr.open('GET',url+"?"+param(op), true);
    xhr.onload = function (e) {
        if (xhr.status === 200) {
            success(xhr.response);
        }
        else{
            error(e.statusText);
        }
    };
    xhr.onerror = function (e) {
        console.error(xhr.statusText);
        error(e);
    };
    xhr.send(null);
  }

  onload(){
   const  _self = this;
   this.s = 0;
   $("rangeMotor").onchange = this.proxy(this.changeRangeMotor,this);
  }

  sendCmd(){
    $("txtMotor").innerHTML = this.s;
    console.log("changeRangeMotor s:"+this.s);

    this.getJson("motor.php",{'s':this.s},
    function(response){
        console.log(response);
    },function(e){
        //console.log(e);
    });
  }

  changeRangeMotor(e){
    this.s = $("rangeMotor").value;
    this.proxy(this.sendCmd,this)();
  }
}

var index = new Index();
window.onload = function(){
    index.onload()
}
```

javascriptからのリクエストを受取PHPファイルです。Pythonへリクエストを中継しています。
```php:motor.php
<?php
    $currentpath = dirname(__FILE__)."/";
    $s = escapeshellarg($_GET["s"]);

    header( "Content-Type: application/json; charset=utf-8" );
    $last_line = system('python3 '.$currentpath.'motor.py '.$s, $answer);
```

DRV8833.py を利用してPHPで受け取ったリクエストを実行してモーターを動かしています。
```python:motor.py
import sys,os
sys.path.append(os.pardir)

import RPi.GPIO as GPIO
from libs import DRV8830
import time
import json
import sys

argvs = sys.argv
s = argvs[1];

result_json = {'status': 'OK','s':s}
print(json.dumps(result_json))

GPIO.setmode(GPIO.BCM)
motor = DRV8830.DRV8830(DRV8830.DRV8830_A1_A0_0_0)

motor.speed(int(s1))
time.sleep(5)

motor.clean()
GPIO.cleanup()

```

## DRV8830 ライブラリサンプル
DRV8830.pyをシンプルに利用したサンプルコード
```python:sample.py
import sys,os
sys.path.append(os.pardir)

import RPi.GPIO as GPIO
from libs import DRV8830
import time

GPIO.setmode(GPIO.BCM)
motor = DRV8830.DRV8830(DRV8830.DRV8830_A1_A0_0_0)

for i in range(-100,100,25):
    motor.speed(i)
    print('motor {0}'.format(i))
    time.sleep(1)

motor.brake()
print('motor brake')

motor.clean()
GPIO.cleanup()
```

1. DRV883(addr) <br> i2cアドレスを指定して初期化
2. speed(s) <br> s : -100 〜 100 負値の場合 逆転
3. brake() <br> モータの回転を停止させる
4. clean() <br> モーターを停止させて、エラーレジスタークリア
