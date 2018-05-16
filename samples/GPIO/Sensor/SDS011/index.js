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
            success( JSON.parse(xhr.response.split("\n")[0]) );
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
   setInterval(this.proxy(this.getSensorValue,this),200);
  }

  getSensorValue(){
    var _self = this;
    // GET sensor.php
    this.getJson("sensor.php",{},
    function(response){
        //console.log(response);
        var pm25 = "---";
        var pm10 = "---";
        if(response.status == true){
            pm25 = response.pm25;
            pm10 = response.pm10;
        }
        //画面更新
        document.getElementById("pm25").innerHTML = pm25;
        document.getElementById("pm10").innerHTML = pm10;
    },function(e){
        //console.log(e);
    });
  }
}

var index = new Index();
window.onload = function(){
    index.onload()
}
