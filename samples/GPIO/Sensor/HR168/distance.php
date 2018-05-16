<?php
    $currentpath = dirname(__FILE__)."/";
    header( "Content-Type: application/json; charset=utf-8" );
    $last_line = system('python '.$currentpath.'distance.py', $answer);
