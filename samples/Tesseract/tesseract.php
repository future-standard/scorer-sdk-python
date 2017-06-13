<?php
  $currentpath = dirname(__FILE__)."/";
  system($currentpath.'saveimg.py', $result);
  if($result==0){
    $data = $_GET['name'];
    if( strcmp($data, "all") == 0 ){
      exec('/opt/scorer/bin/tesseract '.$currentpath.'image/tesseract.bmp stdout 2>/dev/null', $results);
    }else{
      exec('/opt/scorer/bin/tesseract '.$currentpath.'image/tesseract.bmp stdout 2>/dev/null ' .$currentpath.$data.'.conf', $results);
    }

    foreach($results as $result){
      print($result . "\n");
    }
  }
?>
