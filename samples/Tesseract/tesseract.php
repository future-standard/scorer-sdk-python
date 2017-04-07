<?php
  $currentpath = dirname(__FILE__)."/";
  system('python3 '.$currentpath.'saveimg.py', $result);
  if($result==0){
    $data = $_GET['name'];
    if($data==all){
      exec('/opt/scorer/bin/tesseract '.$currentpath.'image/tesseract.bmp stdout 2>/dev/null -tessdata --tessdata-dir '.$currentpath, $results);
    }else{
      exec('/opt/scorer/bin/tesseract '.$currentpath.'image/tesseract.bmp stdout 2>/dev/null -tessdata --tessdata-dir '.$currentpath.' '.$currentpath.$data.'.conf', $results);
    }

    foreach($results as $result){
      print($result . "\n");
    }
  }
?>
