<?php

  // get config
  $home = getenv('HOME');
  $json_file_path = $home . "/scorer-sdk-python/samples/lib/user_roi.json";

  // create json file when received json data
  if(isset($_POST['json'])){
    $json = json_decode($_POST['json']);
    file_put_contents($json_file_path, json_encode($json));
    chmod($json_file_path, 0644);
  }

  echo @file_get_contents($json_file_path);
?>
