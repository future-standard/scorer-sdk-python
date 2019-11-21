<?php

$mainPid = getMainPid();
$monitoringPid = getMonitoringPid();
echo $mainPid.$monitoringPid;

function getMainPid(){
    $cmd = 'pgrep -x thermo';
    return exec($cmd);
}

function getMonitoringPid(){
    $cmd = 'pgrep thermo_moni';
    return exec($cmd);
}

?>