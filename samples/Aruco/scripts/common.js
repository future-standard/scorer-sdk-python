$(function(){
  // canvas object
  var canvas = new fabric.Canvas('canvas');

  // Change size function
  fabric.Object.prototype.resizeToScale = function () {
    setTimeout(function(){
      canvas.renderAll();
      show_text();
    }, 1000);
  }

// Number show
  var show_text = function(){
    var objects = new Array();
    var _objects = canvas.getObjects();
    var canvastext = document.getElementById("canvas_text");
    var context = canvastext.getContext("2d"); 
    context.font = "18pt Arial";
    
    context.clearRect(0, 0, 640, 480);

  }


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
    // alert('off save?');
    $.get('judge.php', {}, function(data){
        alert(data);
    });
  });    


});
