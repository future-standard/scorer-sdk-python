class Index{
  proxy(fn, context){
    return function(){
      return fn.apply(context, arguments);
    };
  }

  getJson(url,op,success,error){
    var param = function(op){
      var queryArray = [];
      Object.keys(op).forEach(function (key) { return queryArray.push(key + '=' + encodeURIComponent(op[key])); });
      return queryArray.join('&');
    };
    var xhr = new XMLHttpRequest();
    xhr.open('GET',url+"?"+param(op), true);
    xhr.onload = function (e) {
        if (xhr.status === 200) {
            success(xhr.response);    
        }
        else{
            error(e.statusText);   
        }
    };
    xhr.onerror = function (e) {
        console.error(xhr.statusText);
        error(e);
    };
    xhr.send(null);
  }
  
  onload(){
   var _self = this;
   var elements = document.getElementsByClassName("btnServo");
   for( var i=0,l=elements.length; l>i; i++ ) {
    elements[i].onclick = _self.proxy( _self.clickBtnServo,_self);
   }
   
   document.getElementById("btnServoAll").onclick = _self.proxy( _self.clickBtnServoAll,_self);
  }
  
  clickBtnServo(e){
    var target = e.currentTarget;
    var c = target.dataset.channel;
    var on = target.dataset.on;
    var off = target.dataset.off;
    target.dataset.off = (off == 600)?150:600;
    
    // GET servo.php?c=0&on=0&off=150
    this.getJson("servo.php",{'c':c,'on':on,'off':off},
    function(response){
        console.log(response);    
    },function(e){
        //console.log(e);
    });
  }
  
  clickBtnServoAll(e){
    var c = 0;
    var on = 0;
    var off = 150;
    var fnc = function(){
        // GET servo.php?c=0&on=0&off=150
        this.getJson("servo.php",{'c':c,'on':on,'off':off},
        function(response){
            console.log(response);    
        },function(e){
            //console.log(e);
        });
        
        if(off == 150){
            c++;
            if(c >= 16) {
                //タイマー停止
                clearInterval(this.timer);
            }
        }
        off = (off==150)?600:150;
    };
    
    this.timer = setInterval(this.proxy(fnc,this),2000);
  }
}

var index = new Index();
window.onload = function(){
    index.onload()
}