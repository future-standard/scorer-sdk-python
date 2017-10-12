<?php
    header( "Content-Type: application/json; charset=utf-8" );
    $last_line = system('python3 '.$currentpath.'distance.py', $answer);
    
    //echo $last_line;
    //echo 'python3 '.$currentpath.'distance.py '.$c;
