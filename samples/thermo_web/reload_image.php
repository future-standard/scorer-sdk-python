<?php

$image_file_path = dirname(__FILE__)."/tempimg.jpg";

if (!file_exists($image_file_path)){
    return;
}

if (!($img = file_get_contents($image_file_path))){
    return;
}
if (!($img_data = base64_encode($img))){
    return;
}
    
echo 'data:image/jpeg;base64,'.$img_data;

?>

