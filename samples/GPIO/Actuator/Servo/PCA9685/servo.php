<?php
    $currentpath = dirname(__FILE__)."/";
    $c = escapeshellarg($_GET["c"]);
    $on = escapeshellarg($_GET["on"]);
    $off = escapeshellarg($_GET["off"]);

    header( "Content-Type: application/json; charset=utf-8" );
    $last_line = system('python3 '.$currentpath.'servo.py '.$c.' '.$on.' '.$off, $answer);
    
    //echo $last_line;
    //echo 'python3 '.$currentpath.'servo.py '.$c.' '.$on.' '.$off;
