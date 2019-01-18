<?php
    if (isset($_POST['search'])) {
        $search = htmlspecialchars($_POST['search']);
        $search_value = $search;
    }else {
        $search = '';
        $search_value = '';
    }
    $images = glob('aws_img/exit/*.jpg');
    //array_multisort(array_map('filemtime', $images), SORT_NUMERIC, SORT_DESC, $images);
    natcasesort($images);
    $images = array_reverse($images);
    $textline = "";
    foreach($images as $file){
        if(is_file($file)){
            $filename = pathinfo($file, PATHINFO_FILENAME);
            $imgline = "<li>" . "　　　　" . $filename . "<br>\n";
            $imgline = $imgline . "<center>\n";
            $enterfile = "aws_img/enter/" . $filename .".jpg";
            $imgline = $imgline . "<a href=\"$enterfile\" data-lightbox=\"exitimages\" data-title=\"$filename\"><img src=\"$enterfile\"></a><br>\n";
            $imgline = $imgline . "<font size=\"5\">&dArr;</font><br><br>\n";
            $imgline = $imgline . "<a href=\"$file\" data-lightbox=\"exitimages\" data-title=\"$filename\"><img src=\"$file\"></a>\n";
            $imgline = $imgline . "<ul class=\"balloon-top\">\n";
            $exif = exif_read_data($enterfile, 'IFD0');
            $exif = exif_read_data($enterfile, 0, true);
            foreach ($exif as $key => $section) {
                if($key == 'EXIF'){
                    foreach ($section as $name => $val) {
                        if($name == 'DateTimeOriginal'){
                            $text = explode(" ", $val);
                            $imgline = $imgline . "<p> Enter Date: $text[0]<br>\n";
                            $imgline = $imgline . "Enter Time: $text[1]<br>\n";
                            $from = strtotime($val);
                        }
                    }
                }
            }
            $exif = exif_read_data($file, 'IFD0');
            $exif = exif_read_data($file, 0, true);
            foreach ($exif as $key => $section) {
                if($key == 'EXIF'){
                    foreach ($section as $name => $val) {
                        if($name == 'DateTimeOriginal'){
                            $text = explode(" ", $val);
                            $imgline = $imgline . "<p> Exit Date: $text[0]<br>\n";
                            $imgline = $imgline . "Exit Time: $text[1]<br>\n";
                            $to = strtotime($val);
                            $dif = $to - $from;
                            $dif_time = gmdate("H:i:s", $dif);
                            $imgline = $imgline . "Staying Time: $dif_time<br>\n";
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
        if($search_value == ''){
            $textline = $textline . $imgline;
        }
        else{
            if(strpos($imgline, $search_value) !== false){
                $textline = $textline . $imgline;
            }
        }
    }
    echo $textline;
?>
