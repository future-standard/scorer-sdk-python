<?php

include('process_check.php');

$pid = getPid();
if ($pid){
  return;
}

$currentpath = dirname(__FILE__)."/";
$json = $currentpath . "/" . "thermo.json";

if( !file_exists($json) ){
    echo "ERR:No ROI File. Please set ROI.\n";
    exit(1);
}

exec('python3 '.$currentpath.'get_roi.py', $result);

$roi_count = count($result);
$roi_args;
for ($i = 0; $i < $roi_count; $i++) {
  $roi_args .= round($result[$i] / 5).' ';
}

$cmd = '/opt/scorer/bin/thermo "'.$currentpath.'" '.$roi_args.'> /dev/null &';
exec($cmd);

$cmd_log = "python3 ./temp_log.py >> /tmp/xxx &";
exec($cmd_log);

?>
