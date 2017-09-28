<?php

$json_file_path = dirname(__FILE__)."/config.json";

$json = $_POST;

file_put_contents($json_file_path, json_encode($json));
chmod($json_file_path, 0644);

?>

