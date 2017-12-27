# DRV8835 デュアルモータードライバー 1.5A サンプル
デュアルモータードライバー DRV8835 を SCORER で利用するためのサンプル

## 接続
| &nbsp; | Raspberry Pi3 | DRV8835 |
|:-----------:|:------------:|:------------:|
| AIN1 | 17 | 16 |
| AIN2 | 18 | 15 |
| BIN1 | 22 |  9 |
| BIN2 | 23 | 10 |
| MODE | GND | 11 |

| &nbsp; | DRV88335 | Motor |
|:-----------:|:------------:|:------------:|
| AOUT1 | 2 | 1 |
| AOUT2 | 4 | 2 |
| BOUT1 | 7 | 1 |
| BOUT2 | 5 | 2 |


![接続した写真](https://raw.githubusercontent.com/tfuru/tf-scorer-actuator/master/Motor/DRV8835/resources/2017-10-02%2014.40.36.jpg?token=ADwbngnxfHWNyukwNNZK_9Sln2ckxC3Vks5Z2w6CwA%3D%3D)

## サンプル実行方法
1. サンプルへのアクセス
http://xxx.xxx.xxx.xxx:20002/samples/Actuator/Motor/DRV8835/
2. 操作方法
ブラウザ画面から DRV88333 に接続したモーターを動かす事ができます。<br>
![画面キャプチャ](https://raw.githubusercontent.com/tfuru/tf-scorer-actuator/master/Motor/DRV8835/resources/2017-10-02%2014.43.54.png?token=ADwbnilbn_8mikclzanGMYam4IAa_9M3ks5Z2w4xwA%3D%3D)

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
   this.s1 = 0;
   this.s2 = 0;
   $("rangeMotor1").onchange = this.proxy(this.changeRangeMotor,this);
   $("rangeMotor2").onchange = this.proxy(this.changeRangeMotor,this);

   //setInterval(this.proxy(this.sendCmd,this),1000);
  }

  sendCmd(){
    $("txtMotor1").innerHTML = this.s1;
    $("txtMotor2").innerHTML = this.s2;
    console.log("changeRangeMotor s1:"+this.s1+" s2:"+this.s2);

    this.getJson("motor.php",{'s1':this.s1,'s2':this.s2},
    function(response){
        console.log(response);    
    },function(e){
        //console.log(e);
    });
  }

  changeRangeMotor(e){
    this.s1 = $("rangeMotor1").value;
    this.s2 = $("rangeMotor2").value;

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
    $s1 = escapeshellarg($_GET["s1"]);
    $s2 = escapeshellarg($_GET["s2"]);

    header( "Content-Type: application/json; charset=utf-8" );
    $last_line = system('python3 '.$currentpath.'motor.py '.$s1.' '.$s2, $answer);
```

DRV8833.py を利用してPHPで受け取ったリクエストを実行してモーターを動かしています。
```python:motor.py
import sys,os
sys.path.append(os.pardir)

import RPi.GPIO as GPIO
from libs import DRV8835
import time
import json
import sys

argvs = sys.argv
s1 = argvs[1];
s2 = argvs[2];

result_json = {'status': 'OK','s1':s1,'s2':s2}
print(json.dumps(result_json))

GPIO.setmode(GPIO.BCM)
motorA = DRV8835.DRV8835(17,18)
motorB = DRV8835.DRV8835(22,23)

motorA.speed(int(s1))
motorB.speed(int(s2))
time.sleep(5)

motorA.clean()
motorB.clean()
GPIO.cleanup()


```

## DRV8835 ライブラリサンプル
DRV8835.pyをシンプルに利用したサンプルコード
```python:sample.py
import sys,os
sys.path.append(os.pardir)

import RPi.GPIO as GPIO
from libs import DRV8835
import time

GPIO.setmode(GPIO.BCM)
motorA = DRV8835.DRV8835(17,18)
motorB = DRV8835.DRV8835(22,23)

for i in range(-100,100,25):
    motorA.speed(i)
    print('motorA {0}'.format(i))
    time.sleep(1)

motorA.brake()
print('motorA brake')

for i in range(-100,100,25):
    motorB.speed(i)
    print('motorB {0}'.format(i))
    time.sleep(1)

motorB.brake()
print('motorB brake')

motorA.clean()
motorB.clean()
GPIO.cleanup()

```

1. DRV885(in1,in2) <br> INポートを指定して初期化
2. speed(s) <br> s : -100 〜 100 負値の場合 逆転
3. brake() <br> モータの回転を停止させる
4. clean() <br> PWMを停止してモーターを停止させる
