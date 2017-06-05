<?php

include('process_check.php');

$pid = getPid();
if ($pid){
  return;
}
$cmd = "./image_judgement.py > /dev/null 2>1&";
exec($cmd);

?>
