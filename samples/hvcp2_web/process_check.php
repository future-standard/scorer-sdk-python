<?php

echo getPid();

function getPid(){
    $cmd = 'pgrep hvcp2_sdk;';
    return exec($cmd);
}

?>