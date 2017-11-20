<?php
    $currentpath = dirname(__FILE__)."/";
    $s = escapeshellarg($_GET["s"]);

    header( "Content-Type: application/json; charset=utf-8" );
    $last_line = system('python3 '.$currentpath.'motor.py '.$s, $answer);

    //echo $answer;
    //echo $last_line;
