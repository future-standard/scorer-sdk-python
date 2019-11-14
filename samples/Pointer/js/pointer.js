//現在のマウス位置を表示する
//function PrintPosition(canvas, message) {
//    var context = canvas.getContext('2d');
//    context.clearRect(0, 0, canvas.width, canvas.height);
//    context.font = '12pt "MSゴシック"';
//    context.fillStyle = 'black';
//    context.fillText(message, 32, 48);
//}

//現在のマウス位置を表示する
function PrintPosition(text, message) {
    document.getElementById(text).innerHTML = message;
}

//現在のマウス位置を取得する
function getMousePosition(canvas, evt) {
    var rect = canvas.getBoundingClientRect();
    return {
        x: evt.clientX - rect.left,
        y: evt.clientY - rect.top
    };
}

//cookieから点の座標情報を取得する
function getPoints(str) {
    var array = []
    var cookie = document.cookie.split(';');
    cookie.forEach(function(value){
        var content = value.split('=');
        if (content[0].trim() == str){
            array = content[1];
            array = array.split(',');
        }
    });
    return array;
}

//1次元配列を2次元配列に変換する
function convert2Array(array) {
    var new_array = [];
    if(array.length != 0){
        //文字列を数値に変換
        for(let i = 0; i < array.length; i++){
            if(i%3 == 2){
                array[i] = (array[i] == 'true') ? true : false;
            }
            else{
                array[i] = Number(array[i]);
            }
        }
        //1次元配列を2次元配列に変換
        for(let i = 0; i < array.length; i=i+3){
            new_array.push([array[i], array[i + 1], array[i + 2]]);
        }
    }
    return new_array;
}

//1次元配列を連想配列に変換する
function convertAssoArray(array) {
    if(array.length != 0){
        //文字列を数値に変換
        for(let i = 0; i < array.length; i++){
            if(i%3 == 2){
                array[i] = (array[i] == 'true') ? true : false;
            }
            else{
                array[i] = Number(array[i]);
            }
        }

        //true, falseを削除
        for(let i = 0; i < array.length; i++){
            if(array[i] == true || array[i] == false){
                array.splice(i, 1)
            }
        }

        //1次元配列から連想配列を作成
        object = {};
        points = [];
        objectnum = 1;
        for(let i = 0; i < array.length; i=i+2){
            points.push({"x":array[i], "y":array[i + 1]})
            if(i%8 == 6){
                object["object" + objectnum] = points;
                points = [];
                objectnum++;
            }
        }
    }
    return object;
}

//操作する点を取得する
function selectPoints(mousePos, array, flag){
    //最短のポイントと距離
    var min_points = [];
    var min_x = 0;
    var min_y = 0;
    var min_distance = 9999;
    //現在保存されているすべての点を参照する
    for(let i = 0; i < array.length; i++){
        //選択状態になっている点があったら保存して解除する
        if(array[i][2] == true && flag == false){
            array[i][2] = false;
        }
        //２点間の距離を計算し、最も現在クリックしている地点に近いものを保存しておく
        distance = Math.sqrt(Math.pow(mousePos.x - array[i][0], 2) + Math.pow(mousePos.y - array[i][1], 2))
        if (distance < min_distance) {
            min_x = array[i][0];
            min_y = array[i][1];
            min_distance = distance;
        }
    }
    //最短距離の点のリストを作成する
    for(let i = 0; i < array.length; i++){
        if (array[i][0] == min_x && array[i][1] == min_y){
            min_points.push(i)
        }
    }
    var obj = new Object();
    obj.array = array;
    obj.points = min_points;
    obj.distance = min_distance;

    return obj;
}

//現在保存されているすべての点を描画する
function drawPoints(canvas, array) {
    var context = canvas.getContext('2d');
    var pointnum = 1;
    var objectnum = 1;
    var firstpoint = []
    var beforepoint = []
    context.font = '12pt "MSゴシック"';

    context.clearRect(0, 0, canvas.width, canvas.height);

    array.forEach(function(value) {
        if (value[2] == true){
            context.fillStyle = 'rgb(192, 80, 77)';
        }
        else{
            context.fillStyle = 'rgb(0, 0, 0)';
        }
        context.fillText(pointnum, value[0] + 10, value[1] + 10);
        context.beginPath();
        context.arc(value[0], value[1], 6, 0,2*Math.PI, true);
        if(pointnum%4 == 1){
            firstpoint = [value[0], value[1]];
        } 
        else{
            if (pointnum%4 == 0) {
                context.moveTo(value[0], value[1]);
                context.lineTo(firstpoint[0], firstpoint[1]);
            }
            context.moveTo(beforepoint[0], beforepoint[1]);
            context.lineTo(value[0], value[1]);
        }
        pointnum++;
        beforepoint = [value[0], value[1]]
        context.stroke();
        context.fill();
    });
}

//画面表示時に実行
function draw() {
    //点を保存する配列を定義
    var array1 = []
    var array2 = []

    //cookieから座標情報を取得
    array1 = getPoints("array1");
    array2 = getPoints("array2");

    //1次元配列を2次元配列に変換
    array1 = convert2Array(array1);
    array2 = convert2Array(array2);

    //キャンバス情報を取得
    var canvas1 = document.getElementById('canvas1');
    if (!(!canvas1 || !canvas1.getContext)){
        drawPoints(canvas1, array1)
        processes(canvas1, array1, 1);
    }

    //キャンバス情報を取得
    var canvas2 = document.getElementById('canvas2');
    if (!(!canvas2 || !canvas2.getContext)){
        drawPoints(canvas2, array2)
        processes(canvas2, array2, 2);
    }
}

//各操作ごとの処理
function processes(canvas, array, num) {
    var flag = false

    //マウスが移動したときの動作
    canvas.addEventListener('mousemove', function (evt) {
        //現在の地点を取得する
        var mousePos = getMousePosition(canvas, evt);
        //現在の地点情報を描画する
        var message = 'Mouse position X:' + mousePos.x + ', Y:' + mousePos.y;
        PrintPosition("text" + num, message);

        //ドラッグしているときの動作
        if (flag == true) {
            //console.log('drag')
            //現在の地点を取得する
            var mousePos = getMousePosition(canvas, evt);
            //現在の地点情報を描画する
            var message = 'Mouse position X:' + mousePos.x + ', Y:' + mousePos.y;
            //PrintPosition(canvas, message);

            //点の選択
            obj = selectPoints(mousePos, array, flag);
            array = obj.array;
            points = obj.points;
            distance = obj.distance;

            //最短の点全てに対して実行
            points.forEach(function(value){
                //最短の点が選択状態だった場合はその位置を更新する
                if (distance < 30 && array[value][2] == true) {
                    array[value][0] = mousePos.x;
                    array[value][1] = mousePos.y;
                    str = array.join(',');
                    document.cookie = 'array' + num + '=' + str;
                }
            });
        }
        //保存されている点を全て描画する
        drawPoints(canvas, array)
    }, false);

    //クリック時の動作
    canvas.addEventListener('click', function (evt) {
        //現在の地点を取得する
        var mousePos = getMousePosition(canvas, evt);
        //現在の地点情報を描画する
        var message = 'Mouse position X:' + mousePos.x + ', Y:' + mousePos.y;
        //PrintPosition(canvas, message);

        //点の選択
        obj = selectPoints(mousePos, array, flag);
        array = obj.array;
        points = obj.points;
        distance = obj.distance;

        //近くに点がある場合
        if (distance < 30) {
            //それらの点を選択状態にする
            points.forEach(function(value){
                array[value][2] = true;
            });
            //shiftを押しながらで重ねて点を打つ
            if ((array.length > 0 && array.length%4 == 3) || evt.shiftKey) {
                array.push([array[points[0]][0], array[points[0]][1], true]);
            }
            str = array.join(',');
            document.cookie = 'array' + num + '=' + str;
        }
        //それ以外の時はその地点を新しい点として保存する
        else {
            array.push([mousePos.x, mousePos.y, true])
            str = array.join(',');
            document.cookie = 'array' + num + '=' + str;
        }
        //保存されている点を全て描画する
        drawPoints(canvas, array)
    }, false);

    //右クリック時の動作
    canvas.addEventListener('contextmenu',function(evt) {
        //最後に保存した点を削除する
        array.pop();
        str = array.join(',');
        document.cookie = 'array' + num + '=' + str;
        //保存されている点を全て描画する
        drawPoints(canvas, array)
    }, false);

    //ドラッグ開始時の動作
    canvas.addEventListener('mousedown',function(evt) {
        //ドラッグ判定をオンにする
        flag = true;
    }, false);

    //ドラッグ終了時の動作
    canvas.addEventListener('mouseup',function(evt) {
        //ドラッグ判定をオフにする
        flag = false;
    }, false);
}

//画像ファイルをアップロードする
function file_upload(file, upload){
    var filepath = document.getElementById(file).value;
    filename = filepath.split('\\').slice(-1)[0]
    document.cookie = file + '=' + filename;

    var formdata = new FormData(document.getElementById(upload));
    var xhttpreq = new XMLHttpRequest();
    xhttpreq.onreadystatechange = function() {
        if (xhttpreq.readyState == 4 && xhttpreq.status == 200) {
            alert(xhttpreq.responseText);
            location.reload()
        }
    };
    xhttpreq.open("POST", "upload.php", true);
    xhttpreq.send(formdata);
}

//json形式で座標情報をダウンロードする
function file_download() {
    var array1 = [];
    var array2 = [];

    //cookieから座標情報を取得する
    array1 = getPoints("array1");
    array2 = getPoints("array2");

    //1次元配列を連想配列に変換する
    var result = {};
    result["image1"] = convertAssoArray(array1);
    result["image2"] = convertAssoArray(array2);

    //連想配列をjson形式に変換してダウンロードする
    const blob = new Blob([JSON.stringify(result, undefined, 1)], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'coordinates.json';
    link.click();
    URL.revokeObjectURL(url);
}
