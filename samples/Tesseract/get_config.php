<?php

$home = getenv('HOME');

$TARGET_FILE='/opt/scorer/home/camera/CONFIG';

$config_file_lines = array();

$config_file_lines = read_config($TARGET_FILE);

function read_config($fname)
{
    $my_config_lines = array();
    $line_num = 0;
    $config_file = fopen($fname, "r");
    if( $config_file ){
        while ($line = fgets($config_file)) {
            if( $line[0] == "#" ){
                continue    ;
            }

            $line_num++;
            $my_config_lines[$line_num] = $line;
        }
    }
    fclose($config_file);
    return $my_config_lines;
}

function get_config($config_file_lines, $variable_name)
{

    foreach( $config_file_lines as $line ) {

        if(strpos($line,$variable_name) !== false){

            $line_comment_deleted = $line;
            if(strpos($line,'#') !== false){
                $line_comment_deleted = strstr($line,'#',true);
            }

            $variable = trim(str_replace($variable_name.'=', '', $line_comment_deleted));
            return $variable;

        }

    }

    return "not found";
}

?>

