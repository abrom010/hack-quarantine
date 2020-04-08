window.onload = function() {
  function httpGet() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", '/storeData', false );
    xmlHttp.send( null );
    return xmlHttp.response;
  }

  function getSize() {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", '/getSize', false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
  }

  let request = httpGet()
  data = JSON.parse(request)
  data = data[0]
  name = data[0]
  address = data[1]
  csz = data[2] + ", " + data[3] + ", " + data[4]

  document.getElementById('storeName').innerHTML = name
  document.getElementById('storeAddress').innerHTML = address
  document.getElementById('csz').innerHTML = csz

  let size = getSize()
  size = size.replace('[', '')
  size = size.replace(']', '')
  document.getElementById('queueSize').innerHTML = size


}
