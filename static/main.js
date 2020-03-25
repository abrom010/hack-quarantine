
//WINDOW.ONLOAD IS CALLED AFTER THE HTML FILE IS LOADED
window.onload = function(){
  let text = "This text was made using Javascript. "
  let url = '/request'

  function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

let data = httpGet(url)

document.getElementById("first_paragraph").innerHTML = text+data;

};
