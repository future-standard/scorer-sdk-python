<!DOCTYPE html>
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
<meta http-equiv="content-script-type" content="text/javascript" />
<meta name="viewport" content="width=768" />
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<link rel="stylesheet" href="css/style.css">
<link href="https://fonts.googleapis.com/earlyaccess/notosansjapanese.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="js/jquery.cookie.js"></script>
<script src="js/tab.js"></script>
<script src="js/pointer.js"></script>
</head>

<body onload="draw()" oncontextmenu="return false;">
    <h1>透視変換座標出力画面</h1>
    <h3>使い方<h3>
    <h4>
    <ol>
    <li>タブで変換前、変換後画像を切り替え。</li>
    <li>ファイル選択で出力したい画像を選択してアップロード。</li>
    <li>何もないところをクリックで点をプロット（4つの点で四角形が構築される）。</li>
    <li>右クリックをすると一番最後にプロットした点を削除。
    <li>点をクリックすると点を選択状態（赤くなる）にできる。その状態で点をドラッグすると点の移動が可能。</li>
    <li>点の上でShiftを押しながらクリックで、同じ座標に点をプロット（二つの四角形を連結できる）。</li>
    <li>ダウンロードボタンをクリックで、現在プロットされている点の座標情報をjson形式で出力。</li>
    </ol>
    </h4>

    <button class="download" type="button" onclick='file_download()'>ダウンロード</button>
    <ul class="tabs">
        <li>
            <input type="radio" class="tab1" name="tabs" id="tab1" value="from" checked/>
            <label for="tab1"><center>変換前</center></label>
            <div id="tab-content1" class="tab-content">
                <form class="upload" id="upload1">
                    <input type="file" id="file1" name="file">
                    <button type="button" onclick='file_upload("file1", "upload1")'>アップロード</button>
                </form>
                <div class="text" id="text1">Mouse position</div>
                <?php
                    include('content1.php')
                ?>
            </div>
        </li>
        <li>
            <input type="radio" class="tab2" name="tabs" id="tab2" value="to"/>
            <label for="tab2"><center>変換後</center></label>
            <div id="tab-content2" class="tab-content">
                <form class="upload" id="upload2">
                    <input type="file" id="file2" name="file">
                    <button type="button" onclick='file_upload("file2", "upload2")'>アップロード</button>
                </form>
                <div class="text" id="text2">Mouse position</div>
                <?php
                    include('content2.php')
                ?>
            </div>
        </li>
    </ul>
</body>
</html>
