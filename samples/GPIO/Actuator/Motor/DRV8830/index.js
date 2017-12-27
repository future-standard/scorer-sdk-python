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
   this.s = 0;
   $("rangeMotor").onchange = this.proxy(this.changeRangeMotor,this);
  }

  sendCmd(){
    $("txtMotor").innerHTML = this.s;
    console.log("changeRangeMotor s:"+this.s);

    this.getJson("motor.php",{'s':this.s},
    function(response){
        console.log(response);
    },function(e){
        //console.log(e);
    });
  }

  changeRangeMotor(e){
    this.s = $("rangeMotor").value;
    this.proxy(this.sendCmd,this)();
  }
}

var index = new Index();
window.onload = function(){
    index.onload()
}
