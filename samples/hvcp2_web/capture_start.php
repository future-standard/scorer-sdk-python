<?php

include('process_check.php');

$pid = getPid();
if ($pid){
  return;
}

$baudrate = $_POST['baudrate'];
$camera_angle = $_POST['camera_angle'];
$image_size = $_POST['image_size'];
$body_detection = $_POST['body_detection'];
$hand_detection = $_POST['hand_detection'];
$face_detection = $_POST['face_detection'];
$face_direction = $_POST['face_direction'];
$age_estimation = $_POST['age_estimation'];
$gender_estimation = $_POST['gender_estimation'];
$gaze_estimation = $_POST['gaze_estimation'];
$blink_estimation = $_POST['blink_estimation'];
$expression_estimation = $_POST['expression_estimation'];
$face_recognition = $_POST['face_recognition'];

$body_detection_threshold = $_POST['body_detection_threshold'];
$hand_detection_threshold = $_POST['hand_detection_threshold'];
$face_detection_threshold = $_POST['face_detection_threshold'];
$face_recognition_threshold = $_POST['face_recognition_threshold'];
$body_detection_size_min = $_POST['body_detection_size_min'];
$body_detection_size_max = $_POST['body_detection_size_max'];
$hand_detection_size_min = $_POST['hand_detection_size_min'];
$hand_detection_size_max = $_POST['hand_detection_size_max'];
$face_detection_size_min = $_POST['face_detection_size_min'];
$face_detection_size_max = $_POST['face_detection_size_max'];
$detection_angle_lr = $_POST['detection_angle_lr'];
$detection_angle_ud = $_POST['detection_angle_ud'];

$stb_tr_retry_count = $_POST['stb_tr_retry_count'];
$stb_tr_pos_steadiness = $_POST['stb_tr_pos_steadiness'];
$stb_tr_size_steadiness = $_POST['stb_tr_size_steadiness'];
$stb_pe_threshold = $_POST['stb_pe_threshold'];
$stb_pe_angle_ud_min = $_POST['stb_pe_angle_ud_min'];
$stb_pe_angle_ud_max = $_POST['stb_pe_angle_ud_max'];
$stb_pe_angle_lr_min = $_POST['stb_pe_angle_lr_min'];
$stb_pe_angle_lr_max = $_POST['stb_pe_angle_lr_max'];
$stb_pe_complete_frame_count = $_POST['stb_pe_complete_frame_count'];
$stb_fr_threshold = $_POST['stb_fr_threshold'];
$stb_fr_angle_ud_min = $_POST['stb_fr_angle_ud_min'];
$stb_fr_angle_ud_max = $_POST['stb_fr_angle_ud_max'];
$stb_fr_angle_lr_min = $_POST['stb_fr_angle_lr_min'];
$stb_fr_angle_lr_max = $_POST['stb_fr_angle_lr_max'];
$stb_fr_complete_frame_count = $_POST['stb_fr_complete_frame_count'];
$stb_fr_min_ratio = $_POST['stb_fr_min_ratio'];

$currentpath = dirname(__FILE__)."/";

$cmd = 'nohup python3 '.$currentpath.'hvcp2_main.py '.
       $baudrate.' '.$camera_angle.' '.$image_size.' '.$body_detection.' '.$hand_detection.' '.$face_detection.' '.$face_direction.' '.$age_estimation.' '.$gender_estimation.' '.$gaze_estimation.' '.$blink_estimation.' '.$expression_estimation.' '.$face_recognition.' '.
       $body_detection_threshold.' '.$hand_detection_threshold.' '.$face_detection_threshold.' '.$face_recognition_threshold.' '.
       $body_detection_size_min.' '.$body_detection_size_max.' '.$hand_detection_size_min.' '.$hand_detection_size_max.' '.$face_detection_size_min.' '.$face_detection_size_max.' '.
       $detection_angle_lr.' '.$detection_angle_ud.' '.
       $stb_tr_retry_count.' '.$stb_tr_pos_steadiness.' '.$stb_tr_size_steadiness.' '.
       $stb_pe_threshold.' '.$stb_pe_angle_ud_min.' '.$stb_pe_angle_ud_max.' '.$stb_pe_angle_lr_min.' '.$stb_pe_angle_lr_max.' '.$stb_pe_complete_frame_count.' '.
       $stb_fr_threshold.' '.$stb_fr_angle_ud_min.' '.$stb_fr_angle_ud_max.' '.$stb_fr_angle_lr_min.' '.$stb_fr_angle_lr_max.' '.$stb_fr_complete_frame_count.' '.$stb_fr_min_ratio. ' >/tmp/hvc_loglog 2>&1  &';

exec($cmd);

?>
