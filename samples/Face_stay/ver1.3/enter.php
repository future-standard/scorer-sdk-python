<?php
    if (isset($_COOKIE["search"])) {
        $search = $_COOKIE["search"];
    }else {
        $search = '';
    }
    $images = glob('aws_img/enter/*.jpg');
    natcasesort($images);
    $images = array_reverse($images);
    $textline = "";
    foreach($images as $file){
        if(is_file($file)){
            $filename = pathinfo($file, PATHINFO_FILENAME);
            $imgline = "<li>" . $filename . "<br>\n";
            $imgline = $imgline . "<center>\n";
            $imgline = $imgline . "<a data-target=\"enter_$filename\" class=\"modal-open\"><img src=\"$file\"></a>\n";
            $exif = exif_read_data($file, 'IFD0');
            $imgline = $imgline . "<ul class=\"balloon-top\">\n";
            $exif = exif_read_data($file, 0, true);
            foreach ($exif as $key => $section) {
                if($key == 'EXIF'){
                    foreach ($section as $name => $val) {
                        if($name == 'DateTimeOriginal'){
                            $text = explode(" ", $val);
                            $imgline = $imgline . "<p> Enter Date: $text[0]<br>\n";
                            $imgline = $imgline .  "Enter Time: $text[1]<br>\n";
                        }
                        if($name == 'UserComment'){
                            $texts = str_replace("ASCII", "", $val);
                            $text = explode(":", $texts);
                            $imgline = $imgline . "Age: $text[0] &#177; $text[1]<br>\n";
                            $imgline = $imgline . "Gender: $text[2]<br></p>\n";
                        }
                    }
                }
            }
            $imgline = $imgline . "</ul>";
            $imgline = $imgline . "</center>";
        }
        $imgline = $imgline . "</li>\n";
        if($search == ''){
            $textline = $textline . $imgline;
        }
        else{
            if(strpos($imgline, $search) !== false){
                $textline = $textline . $imgline;
            }
        }
    }
    echo $textline;
?>
