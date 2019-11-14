<?php
    if (isset($_COOKIE["search"])) {
        $search = $_COOKIE["search"];
    }else {
        $search = '';
    }
    echo "<dt><input type=\"text\" id=\"search\" name=\"search\" value=\"" . $search . "\" placeholder=\"Search\" /></dt>"
?>
