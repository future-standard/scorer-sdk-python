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
<script src="https://cdn.jsdelivr.net/npm/jquery@3/dist/jquery.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="js/slick.min.js"></script>
<script src="js/tab.js"></script>
<script src="js/select.js"></script>
<script src="js/search.js"></script>
<script src="js/jquery.cookie.js"></script>
<script src="js/modal.js"></script>
<script src="js/name.js"></script>
<title>Enter & Exit List</title>
</head>

<body>

<?php
    include('box.php')
?>

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
    <!--
    <li>
        <input type="radio" class="tab3" name="tabs" id="tab3" value="name"/>
        <label for="tab3"><center>Name</center></label>
        <div id="tab-content1" class="tab-content">
        <ul class="tabslide">
        <?php
            include('enter.php')
        ?>
        <ul>
        </div>
    </li>
    -->
</ul>
</form>

<ul class="inputs" name="inputs">
    <dl class="select1">
    <p>
        <h5>In order of</h5>
        <select class="sort" name="sort">
            <option id="sort1" value="early_enter">early entering</option>
            <option id="sort2" value="late_enter">late entering</option>
            <option id="sort3" value="early_exit">early exiting</option>
            <option id="sort4" value="late_exit">late exiting</option>
            <option id="sort5" value="young_age">young age</option>
            <option id="sort6" value="old_age">old age</option>
        </select>
    </p>
    </dl>
    <dl class="search1">
        <?php
            include('search.php')
        ?>
        <dd><button><span></span></button></dd>
    </dl>
</ul>

</body>
</html>
