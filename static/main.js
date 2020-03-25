
//WINDOW.ONLOAD IS CALLED AFTER THE HTML FILE IS LOADED
window.onload = function(){
  var text = "This text was made using Javascript. "
  let url = '/request'

//JQUERY MAKES A GET REQUEST TO THE GIVEN URL AND RUNS THAT FUNCTION
  $.get(url,function(data,status){
    //THIS GETS THE ELEMENT OF THE DOCUMENT BY ID AND MODIFIES THE HTML INSIDE
       document.getElementById("first_paragraph").innerHTML = text+data;
    })

};
