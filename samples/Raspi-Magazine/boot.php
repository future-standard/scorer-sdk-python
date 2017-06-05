<?php
  // load config file
  
  $json_file_path = dirname(__FILE__)."/raspi_magazine.json";

  // create json file when received json data
  if(isset($_POST['json'])){
    $json = json_decode($_POST['json']);
    file_put_contents($json_file_path, json_encode($json));
    chmod($json_file_path, 0644);
  }

  echo @file_get_contents($json_file_path);
