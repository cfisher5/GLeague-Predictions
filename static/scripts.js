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
        if(height < 167){
            console.log("foundone");
            elems[i].style.height = "167px";
        }
    }
}, 3000);

setTimeout(function() {
    var elems = document.getElementsByClassName('main-headshot');
    for (var i = 0; i < elems.length; i++){
        var height = elems[i].clientHeight;
        if(height <= 1){
            console.log("found one");
            elems[i].src = "../static/placeholder.png";
            elems[i].style.width = "126.6px";
        }
    }
}, 6000);

function usePlaceholder(img){
    img.src = "../static/placeholder.png";
    if(img.className === "neighbor-headshot"){
         img.style.width = "100px";
    }
    else if(img.className === "index-headshot"){
        img.style.height = "167px";
    }
    else{
        img.style.height = "157px";
        img.style.width = "125px";
    }


}