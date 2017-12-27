# PCA9685搭載16チャネル PWM/サーボ ドライバー (I2C接続) サンプル
16チャンネルのPWM出力ドライバー を SCORER で利用するためのサンプル

## 接続
| &nbsp; | Raspberry Pi3 | PCA9685 |
|:-----------:|:------------:|:------------:|
| SDA | 3 | 27 |
| SCK | 5 | 26 |

![接続した写真](https://raw.githubusercontent.com/tfuru/tf-scorer-actuator/master/Servo/PCA9685/resources/2017-09-13%2018.03.42.jpg?token=ADwbnnV3EexSUJcfEW2t2z-0wWVVoXUUks5ZwjIrwA%3D%3D)

## サンプル実行方法
1. サンプルへのアクセス
http://xxx.xxx.xxx.xxx:20002/samples/Actuator/Servo/PCA9685/
2. 操作方法
ブラウザ画面からPCA9685に接続した16個のサーボを動かす事ができます。<br>
![16個接続した図](https://raw.githubusercontent.com/tfuru/tf-scorer-actuator/master/Servo/PCA9685/resources/screencapture-192-168-10-13-20002-samples-Actuator-Servo-PCA9685-1505293446962.png?token=ADwbnlFIid_U4aHoRbllW5IiZYT2I2Wcks5ZwjHywA%3D%3D)

## サンプル内容
javascript からのリクエストで 各サーボを駆動させています。
```javascript:index.js
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
   var _self = this;
   var elements = document.getElementsByClassName("btnServo");
   for( var i=0,l=elements.length; l>i; i++ ) {
    elements[i].onclick = _self.proxy( _self.clickBtnServo,_self);
   }
   document.getElementById("btnServoAll").onclick = _self.proxy( _self.clickBtnServoAll,_self);
  }

  clickBtnServo(e){
    var target = e.currentTarget;
    var c = target.dataset.channel;
    var on = target.dataset.on;
    var off = target.dataset.off;
    target.dataset.off = (off == 600)?150:600;

    // GET servo.php?c=0&on=0&off=150
    this.getJson("servo.php",{'c':c,'on':on,'off':off},
    function(response){
        console.log(response);    
    },function(e){
        //console.log(e);
    });
  }
  clickBtnServoAll(e){
    //略
  }
}

var index = new Index();
window.onload = function(){
    index.onload()
}
```

javascriptからのリクエストを受取PHPファイルです。Pythonへリクエストを中継しています。
```php:servo.php
<?php
    $currentpath = dirname(__FILE__)."/";
    $c = escapeshellarg($_GET["c"]);
    $on = escapeshellarg($_GET["on"]);
    $off = escapeshellarg($_GET["off"]);

    header( "Content-Type: application/json; charset=utf-8" );
    $last_line = system('python3 '.$currentpath.'servo.py '.$c.' '.$on.' '.$off, $answer);
```

PCA9685.py を利用してPHPで受け取ったリクエストを実行してサーボを動かしています。
```python:servo.py
from libs import PCA9685
import json
import time  
import sys

argvs = sys.argv
c = argvs[1];
on = argvs[2];
off = argvs[3];

result_json = {'status': 'OK','c':c,'on':on,'off':off}
print(json.dumps(result_json))

pwm = PCA9685.PCA9685(PCA9685.PCA9685_ADDRESS)
pwm.set_pwm_freq(60)

pwm.set_pwm(c, on, off)
time.sleep(0.5)

```

## PCA9685 ライブラリサンプル
PCA9685を シンプルに利用したサンプルコード
```python:sample.py
import sys,os
sys.path.append(os.pardir)

from libs import PCA9685
import time

pwm = PCA9685.PCA9685(PCA9685.PCA9685_ADDRESS)
pwm.set_pwm_freq(60)

servo_min = 150
servo_max = 600

pwm.set_pwm(0, 0, servo_min)
time.sleep(1)

pwm.set_pwm(0, 0, servo_max)
time.sleep(1)

pwm.software_reset()
```

1. PCA9685(i2cAddr) <br> i2c アドレスを設定して初期化
2. set_pwm_freq(freq_hz) <br> freq_hz : PWM周波数を設定
3. set_pwm(channel, on, off) <br> channel : 16個のチャンネルのうち1つを指定 <br> on : PWMパルスのハイセグメントの開始位置 <br> off : PWMパルスのハイセグメントの終了位置
4. software_reset() <br> ソフトウェアリセット
