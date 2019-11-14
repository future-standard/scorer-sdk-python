<?php
    $images = glob('aws_img/enter/*.jpg');
    foreach($images as $file){
        if(is_file($file)){
            $filename = pathinfo($file, PATHINFO_FILENAME);
            $imgline = "<div id=\"enter_$filename\" class=\"modal-content\">\n";
            $imgline = $imgline . "<h1>Name registration</h1>\n";
            $imgline = $imgline . "<center>\n";
            $imgline = $imgline . "<img src=\"$file\">\n";
            $imgline = $imgline . "</center>\n";
            $imgline = $imgline . "<p>Please enter this person's name.</p>\n";
            $imgline = $imgline . "<ul>\n";
            $imgline = $imgline . "<input type=\"text\" id=\"name_regi\" name=\"$file\" value=\"\" size=\"30\" maxlength=\"20\">\n";
            $imgline = $imgline . "</ul>\n";
            $imgline = $imgline . "<a class=\"modal-close\">×</a>\n";
            $imgline = $imgline . "</div>\n";
        }
        echo $imgline;
    }

    $images = glob('aws_img/exit/*.jpg');
    foreach($images as $file){
        if(is_file($file)){
            $filename = pathinfo($file, PATHINFO_FILENAME);
            $imgline = "<div id=\"exit_$filename\" class=\"modal-content\">\n";
            $imgline = $imgline . "<h1>Name registration</h1>\n";
            $imgline = $imgline . "<center>\n";
            $imgline = $imgline . "<img src=\"$file\">\n";
            $imgline = $imgline . "</center>\n";
            $imgline = $imgline . "<p>Please enter this person's name.</p>\n";
            $imgline = $imgline . "<ul>\n";
            $imgline = $imgline . "<input type=\"text\" id=\"name_regi\" name=\"$file\" value=\"\" size=\"30\" maxlength=\"20\">\n";
            $imgline = $imgline . "</ul>\n";
            $imgline = $imgline . "<a class=\"modal-close\">×</a>\n";
            $imgline = $imgline . "</div>\n";
        }
        echo $imgline;
    }
?>
