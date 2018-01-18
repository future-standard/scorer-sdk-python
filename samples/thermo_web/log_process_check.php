<?php

echo getLogPid();

function getLogPid(){
    $cmd = "ps -ef | grep -v grep | grep  'temp_log.py' | awk {'print $2'}";
    return exec($cmd);
}

?>
