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
            elems[i].style.height = "167px";
        }
    }
}, 3000);

setTimeout(function() {
    var elems = document.getElementsByClassName('main-headshot');
    for (var i = 0; i < elems.length; i++){
        var height = elems[i].clientHeight;
        if(height <= 1){
            elems[i].src = "../static/placeholder.png";
            elems[i].style.maxWidth = "267px";
        }
    }
}, 6000);

function usePlaceholder(img){
    img.src = "../static/default-headshot.png";
    img.style.opacity = "0.5";
    if(img.className === "neighbor-headshot"){
         img.style.width = "100px";
    }
    else if(img.className === "index-headshot"){
        img.style.height = "167px";
    }
    else{
        img.style.height = "183px";
    }
}

function check_uncheck_all(btn){
    var d = $(btn).data(); // access the data object of the button
    $(':checkbox').prop('checked', d.checked); // set all checkboxes 'checked' property using '.prop()'
    d.checked = !d.checked; // set the new 'checked' opposite value to the button's data object
}

$(document).ready( function () {
    $('#gamelog_table').DataTable({
        "columnDefs": [
            { "orderable": false, "targets": 18 }
        ],
        "scrollX": true,
        "order": [[ 0, "desc" ]],
        "pagingType": "numbers",
        "pageLength": 10,
        "lengthChange": true,
        "lengthMenu": [[10, 20, 30, -1], [10, 20, 30, "All"]],
        fixedColumns: {
            leftColumns: 1,
            rightColumns: 1
        }

    });
});

function equal_div_heights(){
  var player_info_height = document.getElementById("player_bio").clientHeight;
  document.getElementById("stats").style.minHeight = (player_info_height + 2) + "px";
}

// setInterval(equal_div_heights, 300);

