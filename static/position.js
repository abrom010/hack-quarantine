window.onload = function() {

  function httpGet() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", '/populateTable', false );
    xmlHttp.send( null );
    return xmlHttp.response;
  }

  // var xmlHttp = new XMLHttpRequest();
  let data = httpGet()
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
