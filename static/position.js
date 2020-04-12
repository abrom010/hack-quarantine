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
  for (var i = 1; i<6; i++) {
    id = 'name' + i.toString();
    name = names[i-1]
    if(name!="undefined"){
      console.log("did")
      document.getElementById(id).innerHTML = name
    }
  }

  data = httpGet('/populateCodes/'+num)
  codes = JSON.parse(data)
  for (var i = 1; i<6; i++) {
    id = 'code' + i.toString();
    code = codes[i-1]
    if(code){
      document.getElementById(id).innerHTML = code
    }
  }
  //console.log(fullData)
  //console.log(data)
  // xmlHttp.open( "GET", '/populateTable', false );
  // xmlHttp.send( null );
  // return xmlHttp.response;
}
