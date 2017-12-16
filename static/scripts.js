setTimeout(function() {
    var elems = document.getElementsByClassName('neighbor-headshot');
    for (var i = 0; i < elems.length; i++){
        var height = elems[i].clientHeight;
        if(height < 150){
            elems[i].style.paddingTop = "17px";
        }
    }
}, 1000);

setTimeout(function() {
    var elems = document.getElementsByClassName('index-headshot');
    for (var i = 0; i < elems.length; i++){
        var height = elems[i].clientHeight;
        if(height <= 1){
            console.log("foundone");
            elems[i].src = "../static/placeholder.png";
            elems[i].style.width = "126.6px";
        }
    }
}, 6000);

setTimeout(function() {
    var elems = document.getElementsByClassName('main-headshot');
    for (var i = 0; i < elems.length; i++){
        var height = elems[i].clientHeight;
        if(height <= 1){
            console.log("foundone");
            elems[i].src = "../static/placeholder.png";
            elems[i].style.width = "126.6px";
        }
    }
}, 6000);