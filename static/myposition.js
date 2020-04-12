window.onload = function() {
	function httpPost(theUrl,data) {
	  var xmlHttp = new XMLHttpRequest();
	  xmlHttp.open("POST", theUrl, false );
	  xmlHttp.send( data );
	  return xmlHttp.response;
  }

  let formdata = new FormData()
  num = document.getElementById("id").innerHTML
  code =document.getElementById("code").innerHTML
  formdata.append("id",num)
  formdata.append("code",code)
  url = "/getPosition"
  let request = httpPost(url, formdata)

  data = JSON.parse(request)[0]

  document.getElementById("position").innerHTML = data
}
