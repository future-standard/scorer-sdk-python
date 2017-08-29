<?php

echo getPid();

function getPid(){
    $cmd = 'pgrep thermo;';
    return exec($cmd);
}

?>