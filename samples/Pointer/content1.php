<?php
    if(isset($_COOKIE["file1"])){
        $file = $_COOKIE["file1"];
    }else{
        $file = "";
    }

    if($file != ""){
        list($width, $height) = getimagesize("./images/" . $file);
        echo "<img class=\"image\" id=\"image\" src=\"./images/" . $file . "\"></img>";
        echo "<canvas class=\"canvas\" id=\"canvas1\" width=\"" . $width. "\"height=\"" . $height . "\"></canvas>";
    }
?>
