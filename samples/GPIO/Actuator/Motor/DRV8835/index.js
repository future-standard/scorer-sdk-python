const $ = function(id){return document.getElementById(id);};
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
   const  _self = this;
   this.s1 = 0;
   this.s2 = 0;
   $("rangeMotor1").onchange = this.proxy(this.changeRangeMotor,this);
   $("rangeMotor2").onchange = this.proxy(this.changeRangeMotor,this);
   
   //setInterval(this.proxy(this.sendCmd,this),1000);
  }
  
  sendCmd(){
    $("txtMotor1").innerHTML = this.s1;
    $("txtMotor2").innerHTML = this.s2;
    console.log("changeRangeMotor s1:"+this.s1+" s2:"+this.s2);
    
    this.getJson("motor.php",{'s1':this.s1,'s2':this.s2},
    function(response){
        console.log(response);    
    },function(e){
        //console.log(e);
    });
  }
  
  changeRangeMotor(e){
    this.s1 = $("rangeMotor1").value;
    this.s2 = $("rangeMotor2").value;
    
    this.proxy(this.sendCmd,this)();
  }
}

var index = new Index();
window.onload = function(){
    index.onload()
}