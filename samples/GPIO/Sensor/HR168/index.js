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
   this.baseWidth = 500;
   this.baseFontSize = document.getElementById("distance").style.fontSize;

   setInterval(this.proxy(this.getDistance,this),200);
  }

  //画面更新
  update(p){
    console.log("update p "+p);
    var s =  (this.baseWidth*p);
    console.log("baseWidth "+ this.baseWidth+" s "+s );

    document.getElementById("circle").style.width = s+"px";
    document.getElementById("circle").style.height = s+"px";
    document.getElementById("circle").style.borderRadius = (s/2)+"px"
  }

  getDistance(){
    var _self = this;
    // GET distance.php
    this.getJson("distance.php",{},
    function(response){
        //console.log(response);
        var txt = "----";
        if(response.distance < 0){
            _self.proxy(_self.update,_self)(1);
        }
        else{
            txt = response.distance;
            var p =  (response.distance/response.max);
            _self.proxy(_self.update,_self)(p);
        }
        txt += " mm";
        document.getElementById("distance").innerHTML = txt;
    },function(e){
        //console.log(e);
    });
  }
}

var index = new Index();
window.onload = function(){
    index.onload()
}
