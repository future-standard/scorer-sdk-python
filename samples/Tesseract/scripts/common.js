$(function(){
  // canvas object
  var canvas = new fabric.Canvas('canvas');
  
  // Convert object for Python
  var convert_object = function(object,objname){
    object['id']=objname;
    switch(object['type']){
      case 'rect':
        return convert_rect_object(object,objname);
      break;

    }
  };

  // Convert rect object for Python
  var convert_rect_object = function(object,objname){
    var start = { x: object.left, y: object.top };
    var end_x = object.left + object.width;
    var end_y = object.top + object.height;
    var end = { x: end_x, y: end_y};  
    var id = objname;
    return {
      type: 'rect',
      id: objname,
      width: object.width,
      height: object.height,
      points: [start, end]
    };
  };

  // Remove background image objects
  var remove_background_image = function(object){
    console.log('remove_background_image', object);
    return object;
  };

  // Draw rect
  $('.rect').on('click', function(){
    var rect = new fabric.Rect({
      left: 50,
      top: 50,
      width: 100,
      height: 100,
      fill: 'rgba(0, 0, 255, 0.5)',
      stroke: 'blue',
      strokeWidth: 3,
      padding: 10,
      scaleX: 1,
      scaleY: 1,
      hasRotatingPoint: false
    });

    canvas.add(rect);
    show_text();
  });

  // Change size function
  fabric.Object.prototype.resizeToScale = function () {
    switch (this.type) {
        case "rect":
            this.width *= this.scaleX;
            this.height *= this.scaleY;
            this.scaleX = 1;
            this.scaleY = 1;
          break;
        default:
            break;
    }
    setTimeout(function(){
      canvas.renderAll();
      show_text();
    }, 1000);
  }

// Number show
  var show_text = function(){
    var objects = new Array();
    var _objects = canvas.getObjects();
    var circle_num = 0;
    var line_num = 0;
    var rect_num = 0;
    var canvastext = document.getElementById("canvas_text");
    var context = canvastext.getContext("2d"); 
    context.font = "18pt Arial";
    
    context.clearRect(0, 0, 640, 480);
    for(var i = 0; i < _objects.length; ++i){
      //console.log(_objects[i]['type']);
      
      switch(_objects[i]['type']){
          case 'rect':
            context.fillStyle = 'yellow';
            //context.fillText("rect" + rect_num, _objects[i]['left']+_objects[i]['width']/2, _objects[i]['top']+_objects[i]['height']/2);
            context.fillText("rect" + rect_num, _objects[i]['left'], _objects[i]['top']);
            rect_num++;
          break;
      }      
    }
  }

  // Output json file
  $('.json').on('click', function(){
    var objects = new Array();
    var _objects = canvas.getObjects();
    var circle_num = 0;
    var line_num = 0;
    var rect_num = 0;
    
    for(var i = 0; i < _objects.length; ++i){

      switch(_objects[i]['type']){
          case 'rect':
            objects.push(convert_object(_objects[i],"rect" + rect_num));
            rect_num++;
          break;
      }
    }

    $.post('boot.php', { json: JSON.stringify({objects: (objects), _canvas: JSON.stringify(canvas)}) }, function(data){
      if(data == null || data == ""){
        alert('failed');
      } else {
        alert('Success');
      }
    });
  });

  // Load json file
  $('.load_json').on('click', function(){
    // Get json file
    $.get('boot.php', {}, function(data){
      canvas.loadFromJSON(data['_canvas']);
      if(data == null || data == ""){
        alert('failed');
      }
    }, 'json');
    show_text();
  }).click();

  // Delete objects
  $('.delete').on('click', function(){
    deleteObjects();
    show_text();
  });

  // Change scale
  function deleteObjects(){
    var activeObject = canvas.getActiveObject(),
    activeGroup = canvas.getActiveGroup();
    if (activeObject) {
      canvas.remove(activeObject);
    } else if (activeGroup) {
      var objectsInGroup = activeGroup.getObjects();
      canvas.discardActiveGroup();
      objectsInGroup.forEach(function(object) {
        canvas.remove(object);
      });
    }
    show_text();
  }
  canvas.on('object:modified', function (e) {
    var _objects = canvas.getObjects();
    for(var i = 0; i < _objects.length; ++i){
      _objects[i].resizeToScale();
    }
  });
  canvas.on('mouse:up', function (e) {
    canvas.trigger('object:modified');
  });

  // down delete key
  $(window).keyup(function(e){
    if(e.keyCode != 72 && $('.display').val() == 'Show'){
      return;
    }
    switch(e.keyCode){
      case 8:
      case 46:
        // delete key
        deleteObjects();
      break;

      case 72:
        $('.display').click();
      break;

      case 82:
        // L key
        $('.rect').click();
      break;

      case 83:
        // S key
        $('.json').click();
      break;

      case 73:
        // I key
        $('.load_json').click();
      break;
    }
  });

  // display
  var _tmp_canvas = '';
  $('.display').on('click', function(){
    if($(this).val() == 'Show'){
      $(this).val('Hide');
      $('input:not(.display)').prop('disabled', false);
      canvas.loadFromJSON(_tmp_canvas);
    } else {
      $(this).val('Show');
      $('input:not(.display)').prop('disabled', true);

      _tmp_canvas = canvas.toJSON();
      
      canvas.clear();
      canvas.setBackgroundImage(_background_image, canvas.renderAll.bind(canvas), {
          backgroundImageStretch: true
      });
    }
    canvas.renderAll();
    show_text();
  });

  // Draw background images
  var _background_image;
  setInterval(function(){
      show_text();
      $.ajax({
      url: "reload_image.php"
  }).done(function(data){
    _background_image = data.replace('<figure><img src="', '').replace('" class="active" alt="video0-latest" height="240" width="320" /><figcaption>video0-latest</figcaption></figure>', '').replace('" class="active" alt="video0-latest" height="480" width="640" /><figcaption>video0-latest</figcaption></figure>', '');
    canvas.setBackgroundImage(_background_image, canvas.renderAll.bind(canvas), {
        backgroundImageStretch: true
    });
    
  });
  show_text();

  }, 1000);
  
  // Judge 
  $('.judge').on('click', function(){
    //alert('off save?');
    var selindex = document.form1.character.value;
    $.get('tesseract.php', {name: selindex}, function(data){
      if(data == null || data == ""){
        alert('failed');
      } else {
        alert(data);
      }
    });
  });    


});
