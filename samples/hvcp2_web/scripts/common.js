$(function(){
  
  ProcessCheckFunc();
  
  // Load config
  $.ajax({
    type: 'POST',
    datatype: 'json',
    url: "config_load.php",
  }).done(function(data){
    if(data){
      var json = JSON.parse(data);
      SetConfiguration(json);
    }
  });
  
  // Validate input value
  $('input[type=number]').on('input', function(){
    if (!isValidValue($(this)))
    {
      $(this).css('background-color', 'orange');
    }
    else
    {
      $(this).css('background-color', '');
    }
  });

  // Start 
  $('#status').on('click', '.start', function(){
    // Check input value
    var isValid = true;
    $('input[type=number]').each(function(){
      if (!isValidValue($(this)))
      {
        isValid = false;
        return false;
      }
    });
    if (!isValid)
    {
      alert('Configuration value is invalid.');
      return;
    }

    var json = GetConfiguration();

    // Save config
    $.ajax({
      type: 'POST',
      datatype: 'json',
      url: "config_save.php",
      data: json
    }).done(function(data){ });
    
    // Start process
    $.ajax({
      type: 'POST',
      datatype: 'json',
      url: "capture_start.php",
      data: json
    }).done(function(data){ });
  });

  // Stop
  $('#status').on('click', '.stop', function(){
    $.ajax({
      url: "capture_stop.php"
    }).done(function(data){ });
  });

  // Advanced Configuration
  $('.toggle').click(function(){
    $(this).toggleClass("active").next().slideToggle(500);
  });

  // Reload Proc
  setInterval(function(){
    $('img').attr('src', 'hvcp2.bmp?r=' + Math.random());

    $.ajax({
      url: "reload_log.php"
    }).done(function(data){
      $('.log pre').html(data);
    });

    ProcessCheckFunc();

  }, 500);


  function ProcessCheckFunc(){
    $.ajax({
      url: "process_check.php"
    }).done(function(data){
      var span = $("#status span");
      var button = $("#status button");
      var input = $('.gallery input');
      if (data){
        // camera process alive
        if (button.hasClass('start')){
          span.text("Started / ");
          button.attr('class', "stop");
          button.text("Stop");
          input.prop('disabled', true);
        }
      }
      else{
        // camera process dead
        if (button.hasClass('stop')){
          span.text("Stopped / ");
          button.attr('class', "start");
          button.text("Start");
          input.prop('disabled', false);
        }
      }
    });
  }
  
  function GetConfiguration(){
    var json = {
      baudrate: $('input[name=baudrate]:checked').val(),
      camera_angle: $('input[name=camera_angle]:checked').val(),
      image_size: $('input[name=image_size]:checked').val(),
      body_detection: $('input[name=body_detection]:checked').val(),
      hand_detection: $('input[name=hand_detection]:checked').val(),
      face_detection: $('input[name=face_detection]:checked').val(),
      face_direction: $('input[name=face_direction]:checked').val(),
      age_estimation: $('input[name=age_estimation]:checked').val(),
      gender_estimation: $('input[name=gender_estimation]:checked').val(),
      gaze_estimation: $('input[name=gaze_estimation]:checked').val(),
      blink_estimation: $('input[name=blink_estimation]:checked').val(),
      expression_estimation: $('input[name=expression_estimation]:checked').val(),
      face_recognition: $('input[name=face_recognition]:checked').val(),
      
      body_detection_threshold: $('#body_detection_threshold').val(),
      hand_detection_threshold: $('#hand_detection_threshold').val(),
      face_detection_threshold: $('#face_detection_threshold').val(),
      face_recognition_threshold: $('#face_recognition_threshold').val(),
      body_detection_size_min: $('#body_detection_size_min').val(),
      body_detection_size_max: $('#body_detection_size_max').val(),
      hand_detection_size_min: $('#hand_detection_size_min').val(),
      hand_detection_size_max: $('#hand_detection_size_max').val(),
      face_detection_size_min: $('#face_detection_size_min').val(),
      face_detection_size_max: $('#face_detection_size_max').val(),
      detection_angle_lr: $('input[name=detection_angle_lr]:checked').val(),
      detection_angle_ud: $('input[name=detection_angle_ud]:checked').val(),

      stb_pe_complete_frame_count: $('#stb_pe_complete_frame_count').val(),
      stb_pe_threshold: $('#stb_pe_threshold').val(),
      stb_pe_angle_ud_min: $('#stb_pe_angle_ud_min').val(),
      stb_pe_angle_ud_max: $('#stb_pe_angle_ud_max').val(),
      stb_pe_angle_lr_min: $('#stb_pe_angle_lr_min').val(),
      stb_pe_angle_lr_max: $('#stb_pe_angle_lr_max').val(),
      stb_fr_complete_frame_count: $('#stb_fr_complete_frame_count').val(),
      stb_fr_threshold: $('#stb_fr_threshold').val(),
      stb_fr_angle_ud_min: $('#stb_fr_angle_ud_min').val(),
      stb_fr_angle_ud_max: $('#stb_fr_angle_ud_max').val(),
      stb_fr_angle_lr_min: $('#stb_fr_angle_lr_min').val(),
      stb_fr_angle_lr_max: $('#stb_fr_angle_lr_max').val(),
      stb_fr_min_ratio: $('#stb_fr_min_ratio').val(),
      stb_tr_retry_count: $('#stb_tr_retry_count').val(),
      stb_tr_pos_steadiness: $('#stb_tr_pos_steadiness').val(),
      stb_tr_size_steadiness: $('#stb_tr_size_steadiness').val(),
    };
    return json;
  }
  
  function SetConfiguration(json){
    $('input[name=baudrate]').val([json['baudrate']]);
    $('input[name=camera_angle]').val([json['camera_angle']]);
    $('input[name=image_size]').val([json['image_size']]);
    $('input[name=body_detection]').val([json['body_detection']]);
    $('input[name=hand_detection]').val([json['hand_detection']]);
    $('input[name=face_detection]').val([json['face_detection']]);
    $('input[name=face_direction]').val([json['face_direction']]);
    $('input[name=age_estimation]').val([json['age_estimation']]);
    $('input[name=gender_estimation]').val([json['gender_estimation']]);
    $('input[name=gaze_estimation]').val([json['gaze_estimation']]);
    $('input[name=blink_estimation]').val([json['blink_estimation']]);
    $('input[name=expression_estimation]').val([json['expression_estimation']]);
    $('input[name=face_recognition]').val([json['face_recognition']]);
    
    $('#body_detection_threshold').val(json['body_detection_threshold']);
    $('#hand_detection_threshold').val(json['hand_detection_threshold']);
    $('#face_detection_threshold').val(json['face_detection_threshold']);
    $('#face_recognition_threshold').val(json['face_recognition_threshold']);
    $('#body_detection_size_min').val(json['body_detection_size_min']);
    $('#body_detection_size_max').val(json['body_detection_size_max']);
    $('#hand_detection_size_min').val(json['hand_detection_size_min']);
    $('#hand_detection_size_max').val(json['hand_detection_size_max']);
    $('#face_detection_size_min').val(json['face_detection_size_min']);
    $('#face_detection_size_max').val(json['face_detection_size_max']);
    $('input[name=detection_angle_lr]').val([json['detection_angle_lr']]);
    $('input[name=detection_angle_ud]').val([json['detection_angle_ud']]);

    $('#stb_pe_complete_frame_count').val(json['stb_pe_complete_frame_count']);
    $('#stb_pe_threshold').val(json['stb_pe_threshold']);
    $('#stb_pe_angle_ud_min').val(json['stb_pe_angle_ud_min']);
    $('#stb_pe_angle_ud_max').val(json['stb_pe_angle_ud_max']);
    $('#stb_pe_angle_lr_min').val(json['stb_pe_angle_lr_min']);
    $('#stb_pe_angle_lr_max').val(json['stb_pe_angle_lr_max']);
    $('#stb_fr_complete_frame_count').val(json['stb_fr_complete_frame_count']);
    $('#stb_fr_threshold').val(json['stb_fr_threshold']);
    $('#stb_fr_angle_ud_min').val(json['stb_fr_angle_ud_min']);
    $('#stb_fr_angle_ud_max').val(json['stb_fr_angle_ud_max']);
    $('#stb_fr_angle_lr_min').val(json['stb_fr_angle_lr_min']);
    $('#stb_fr_angle_lr_max').val(json['stb_fr_angle_lr_max']);
    $('#stb_fr_min_ratio').val(json['stb_fr_min_ratio']);
    $('#stb_tr_retry_count').val(json['stb_tr_retry_count']);
    $('#stb_tr_pos_steadiness').val(json['stb_tr_pos_steadiness']);
    $('#stb_tr_size_steadiness').val(json['stb_tr_size_steadiness']);
  }

  function isInteger(x){
    return Math.round(x) === x;
  }
  
  function isValidValue(elm){
    if (isNaN(parseInt(elm.val(), 10))){
      // Not numerical value
      return false;
    }
    
    var val = Number(elm.val());
    var min = Number(elm.attr('min'));
    var max = Number(elm.attr('max'));

    return (isInteger(val) && min <= val && val <= max);
  }

});


