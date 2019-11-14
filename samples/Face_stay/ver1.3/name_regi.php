<?php
mb_language("ja");
mb_internal_encoding("UTF-8");

$imgpath = $_POST['imgpath'];
$name = $_POST['name'];

$command = "export LANG=ja_JP.UTF-8; python3 name_regi.py " . $imgpath . " " . $name;
exec($command, $output);
echo json_encode($output);
?>
