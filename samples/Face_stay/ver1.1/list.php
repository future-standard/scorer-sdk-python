<!DOCTYPE html>
<html lang="ja">
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8" />
<meta http-equiv="content-script-type" content="text/javascript" />
<meta name="viewport" content="width=768" />
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<link href="https://fonts.googleapis.com/earlyaccess/notosansjapanese.css" rel="stylesheet" />
<link rel="stylesheet" href="js/slick.css">
<link rel="stylesheet" href="js/slick-theme.css">
<link rel="stylesheet" href="css/slider.css">
<link rel="stylesheet" href="css/balloon.css">
<link rel="stylesheet" href="css/style.css">
<link rel="stylesheet" href="css/lightbox.css">
<script src="https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="js/slick.min.js"></script>
<script src="js/tab.js"></script>
<script src="js/jquery.cookie.js"></script>
<script src="js/lightbox.js"></script>
<title>Enter & Exit List</title>
</head>

<body>
<h1>Enter & Exit List</h1>
<form>
<ul class="tabs">
    <li>
        <input type="radio" class="tab1" name="tabs" id="tab1" value="enter" checked/>
        <label for="tab1"><center>Enter</center></label>
        <div id="tab-content1" class="tab-content">
        <ul class="tabslide">
        <?php
            include('enter.php')
        ?>
        <ul>
        </div>
    </li>

    <li>
        <input type="radio" class="tab2" name="tabs" id="tab2" value="exit"/>
        <label for="tab2"><center>Exit</center></label>
        <div id="tab-content2" class="tab-content">
        <ul class="tabslide2">
        <?php
            include('exit.php')
        ?>
        </ul>
        </div>
    </li>
</ul>

</form>
    <form action="./list.php" name="search1" method="post">
        <dl class="search1">
            <?php
                include('search.php')
            ?>
            <dd><button><span></span></button></dd>
        </dl>
    </form>

</body>
</html>
