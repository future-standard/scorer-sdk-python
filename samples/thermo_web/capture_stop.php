<?php

include('process_check.php');
include('log_process_check.php');

$pid = getPid();
if ($pid){
    exec('kill -9 '.$pid);
}

$log_pid = getLogPid();
if ($log_pid){
    exec('kill -9 '.$log_pid);
}



?>
