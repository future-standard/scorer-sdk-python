<?php
    $currentpath = dirname(__FILE__)."/";
    $s1 = escapeshellarg($_GET["s1"]);
    $s2 = escapeshellarg($_GET["s2"]);

    header( "Content-Type: application/json; charset=utf-8" );
    $last_line = system('python3 '.$currentpath.'motor.py '.$s1.' '.$s2, $answer);
    
    //echo $answer;
    //echo $last_line;