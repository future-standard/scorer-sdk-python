<?php

include('process_check.php');

$main_pid = getMainPid();
if ($main_pid){
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

$monitoring_pid = getMonitoringPid();
if (!$monitoring_pid){
  $cmd = '/opt/scorer/bin/thermo_monitoring > /dev/null &';
  exec($cmd);
}

$cmd_log = "python3 ./temp_log.py >> /tmp/xxx &";
exec($cmd_log);

?>
