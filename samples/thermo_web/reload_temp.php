<?php

$json_file_path = dirname(__FILE__)."/tempdata.json";

if (!file_exists($json_file_path)){
    return;
}

$json = @file_get_contents($json_file_path);
$arr = json_decode($json, true);

echo '<p>'.sprintf('======== Temperature at %s ========', date('Y/m/d H:i:s', strtotime($arr['Time']))).'</p>';
if ($arr['Stable'] == 'true'){
    echo '<p class="stable">temperature is stable now.</p>';
}
else{
    echo '<p class="unstable">temperature is unstable now.</p>';
}
echo '<p>'.getTempText('Whole', $arr['Whole']).'</p>';

$roi_count = count($arr['ROI']);
for($i = 0; $i < $roi_count; $i++) {
    $name = 'Rect'.$i;
    if ($arr['ROI'][$name]){
        echo '<p>'.getTempText($name, $arr['ROI'][$name]).'</p>';
    }
}

function getTempText($name, $temp){
    return sprintf('【%s】 max:%6.2f [C] , min:%6.2f [C] , avg:%6.2f [C]', $name, $temp['max'], $temp['min'], $temp['avg']);
}

?>

