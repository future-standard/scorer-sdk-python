<?php
    if(isset($_COOKIE["file2"])){
        $file = $_COOKIE["file2"];
    }else{
        $file = "";
    }

    if($file != ""){
        list($width, $height) = getimagesize("./images/" . $file);
        echo "<img class=\"image\" id=\"image\" src=\"./images/" . $file . "\"></img>";
        echo "<canvas class=\"canvas\" id=\"canvas2\" width=\"" . $width. "\"height=\"" . $height . "\"></canvas>";
    }
?>
