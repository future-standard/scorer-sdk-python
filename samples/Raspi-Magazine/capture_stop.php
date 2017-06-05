<?php

include('process_check.php');

$pid = getPid();
if (!$pid){
    return;
}

exec('kill '.$pid);

?>
