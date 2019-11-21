<?php

include('process_check.php');
include('log_process_check.php');

$monitoring_pid = getMonitoringPid();
if ($monitoring_pid){
    exec('kill -9 '.$monitoring_pid);
}

$main_pid = getMainPid();
if ($main_pid){
    exec('kill -9 '.$main_pid);
}

$log_pid = getLogPid();
if ($log_pid){
    exec('kill -9 '.$log_pid);
}

?>
