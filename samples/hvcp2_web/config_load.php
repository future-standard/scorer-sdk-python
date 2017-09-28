<?php

$json_file_path = dirname(__FILE__)."/config.json";

if (!file_exists($json_file_path)){
    return;
}

$json = @file_get_contents($json_file_path);
echo $json

?>

