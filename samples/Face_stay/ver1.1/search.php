<?php
    if (isset($_POST['search'])) {
        $search = htmlspecialchars($_POST['search']);
        $search_value = $search;
    }else {
        $search = '';
        $search_value = '';
    }
    echo "<dt><input type=\"text\" name=\"search\" value=\"". $search_value . "\" placeholder=\"Search\" /></dt>"
?>
