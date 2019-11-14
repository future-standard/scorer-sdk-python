<?php
    $file_tmp  = $_FILES["file"]["tmp_name"];
    $file_save = "./images/" . $_FILES["file"]["name"];
    $result = @move_uploaded_file($file_tmp, $file_save);

    if ($result === true) {
        echo "UPLOAD OK";
    } 
    else {
        echo "UPLOAD NG";
    }
?>
