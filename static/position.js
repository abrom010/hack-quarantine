window.onload = function() {

  function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.response;
  }

  num = document.getElementById("id").innerHTML
  // var xmlHttp = new XMLHttpRequest();
  let data = httpGet('/populateNames/'+num)
  names = JSON.parse(data)
  for (var i = 1; i<names.length; i++) {
    id = 'name' + i.toString();
    document.getElementById(id).innerHTML = names[i - 1]
  }

  data = httpGet('/populateCodes/'+num)
  codes = JSON.parse(data)
  for (var i = 1; i<codes.length; i++) {
    id = 'code' + i.toString();
    document.getElementById(id).innerHTML = codes[i - 1]
  }
  //console.log(fullData)
  //console.log(data)
  // xmlHttp.open( "GET", '/populateTable', false );
  // xmlHttp.send( null );
  // return xmlHttp.response;
}
