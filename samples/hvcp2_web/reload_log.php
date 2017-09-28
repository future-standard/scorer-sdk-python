<?php

$text_file_path = dirname(__FILE__)."/log.txt";

if (!file_exists($text_file_path)){
    return;
}

$text = @file_get_contents($text_file_path);
echo $text

?>
