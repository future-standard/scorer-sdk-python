<?php

// set the absolute path to the directory containing the images
define ('LOGFILE', 'marker');
define ('TAIL_LENGTH', 30);
define ('IMGDIR', '/mnt/scorer_core');

// get image files from directory
list($img_names, $img_types, $img_data, $file_stats) = get_images(IMGDIR);

function get_images($dir_name)
{
    $img_names = array();
    $img_types = array();
    $img_data = array();
    $file_stats = array();

    $dh = opendir($dir_name);
    if (false == $dh)
        return array($img_names, $img_types, $img_data, $file_stats);

    $temp_fname = array();  // Temporary store
    while (false != ($fname = readdir($dh)))
    {
        if (false != ($stat = stat($dir_name .'/'. $fname))) {
            if (($stat['mode'] & 0100000) == 0)
                continue;

            $file_stats[$fname] = array('mtime' => $stat['mtime'],
                                        'size' => $stat['size']);

            if (preg_match('/^.*-latest\.(jpg|png)$/i', $fname))
                $temp_fname[] = $fname;
        }
    }
    closedir($dh);

    ksort($file_stats);
    sort($temp_fname);

    foreach ($temp_fname as &$fname)
    {
        if (false == ($img = file_get_contents($dir_name .'/'. $fname)))
            continue;
        if (false == ($imgstr = base64_encode($img)))
            continue;

        if (preg_match('/jpg$/', $fname)) {
            $img_names[] = str_replace(".jpg", "", $fname);
            $img_types[] = "data:image/jpeg;base64";
        }
        else {
            $img_names[] = str_replace(".png", "", $fname);
            $img_types[] = "data:image/png;base64";
        }
        $img_data[] = $imgstr;
    }

    return array($img_names, $img_types, $img_data, $file_stats);
}

?>

