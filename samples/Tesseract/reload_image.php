<?php

include('get_image.php');
include('get_config.php');

$width = get_config($config_file_lines,'VIDEO_WIDTH');
$height = get_config($config_file_lines,'VIDEO_HEIGHT');
$n = count($img_names);

for($i = 0; $i < $n; $i++) {
    echo '<figure>';
    echo '<img src="data:image/jpeg;base64,'. $img_data[$i] .
         '" class="active" alt="' . $img_names[$i] . '" height="' . $height . '" width="' . $width . '" />';
    echo '<figcaption>' . $img_names[$i] . '</figcaption>';
    echo '</figure>';
}
?>

