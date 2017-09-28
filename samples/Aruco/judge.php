<?php
  $currentpath = dirname(__FILE__)."/";
  exec('python3 '.$currentpath.'readAR.py '.$currentpath.'intrinsics.yml', $results);
  
  foreach($results as $result){
    print($result . "\n");
  }
?>
