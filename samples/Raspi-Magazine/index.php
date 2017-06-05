<html>
 <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=800px">
    <script src="/samples/scripts/jquery-3.2.1.min.js"></script>
    <script src="/samples/scripts/fabric.min.js"></script>
    <script src="./scripts/common.js" type="text/javascript"></script>
    <link rel="stylesheet" type="text/css" href="./scripts/common.css" />
 </head>
 <body>
  <div>
    <div style="width: 640px; margin: 30px auto 0; position:relative ">
      <canvas width="640" height="480" style="position: relative;" id="canvas"></canvas>
      <canvas width="640" height="480" style="position: absolute;z-index: 2;top: 0;pointer-events: none;" id="canvas_text"></canvas>
    </div>
    <div style="text-align: center; margin: 10px 0">
      <input type="button" class="display" value="Hide" name="">
      <input type="button" class="rect" value="Rect" name="">
      <input type="button" class="delete" value="Remove" name="">
      <input type="button" class="json" value="Save" name="">
      <input type="button" class="load_json" value="Load" name="">
    </div>
    <div  style="text-align: center; margin: 10px 10px">
            <input type="button" class="target" value="Target" name="">
            <?php 
            if(file_exists ("image/target.png") == True ){
            ?>
                <img class="targetimg" src="image/target.png">
            <?php 
            }else{
            ?>
                <img class="targetimg" width=60 height=60 src="">
            <?php 
            }
            ?>
    </div>

    <div id="status" style="text-align: center; margin: 10px 0">
      <span>Stopped / </span>
      <button type="button" class="start" value="Target">Start</button>
    </div>
    <div id="result" style="text-align: center; margin: 10px 0"></div>


    <div style="margin-left: 320px">
      <h3>使い方</h3>
      <p>
        このWEBアプリはスイッチのON状態を画像であらかじめ記録し、現在のターゲット位置の<br>
        画像がON状態と同じ場合は、画面キャプチャを保存するWebアプリです。
        <ol>
          <li>Rectを選択</li>
          <li>表示された「rect0」をスイッチの位置に合わせサイズを調整する</li>
          <li>「Save」をおして、エリアを確定させる</li>
        </ol>
      </p>
    </div>
    
  </div>
 </body>
</html>


