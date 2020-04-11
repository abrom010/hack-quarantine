window.onload = function() {

  function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.response;
  }

  num = document.getElementById("id").innerHTML
  // var xmlHttp = new XMLHttpRequest();
  let data = httpGet('/populateTable/'+num)
  names = JSON.parse(data)
  for (var i = 1; i<names.length + 1; i++) {
    // console.log(i.toString())
    id = 'name' + i.toString();
    document.getElementById(id).innerHTML = names[i - 1]
  }
  //console.log(fullData)
  //console.log(data)
  // xmlHttp.open( "GET", '/populateTable', false );
  // xmlHttp.send( null );
  // return xmlHttp.response;
}
