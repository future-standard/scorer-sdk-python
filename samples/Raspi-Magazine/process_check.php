<?php

echo getPid();

function getPid(){
    $cmd = "ps -e | grep -v grep | grep image_judgement  | awk '{print $1}' ";
    return exec($cmd);
}

?>
