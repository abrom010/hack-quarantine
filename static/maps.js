wvar map;
var service;
var infoWindow;
var geocoder;
var autocomplete;
var markers = [];

function httpGet(theUrl) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "GET", theUrl, false );
  xmlHttp.send( null );
  return xmlHttp.response;
}

function httpPost(theUrl,data) {
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open("POST", theUrl, false );
  xmlHttp.send( data );
  return xmlHttp.response;
}

function initMap() {
  var latlong = new google.maps.LatLng(0, 0);
  var mapOptions = {
      zoom: 3,
      center: latlong,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }

  map = new google.maps.Map(
      document.getElementById('map'), mapOptions);

  autocomplete = new google.maps.places.Autocomplete(document.getElementById('autocomplete'));
  autocomplete.addListener('place_changed', onPlaceChanged);

  places = new google.maps.places.PlacesService(map);

  addresses_to_markers();

  map.addListener('bounds_changed',search)
  map.addListener('zoom_changed',search)

  infoWindow = new google.maps.InfoWindow({
      content: document.getElementById('info-content')
  });
}

function onPlaceChanged() {
  console.log('place changed')
  var place = autocomplete.getPlace();
  if (place.geometry) {
    map.panTo(place.geometry.location);
    map.setZoom(10);
    search();
  } else {
    document.getElementById('autocomplete').placeholder = 'Enter a city';
  }
}

function search() {
  bounds = map.getBounds();
  zoom = map.getZoom();

  for(var i = 0; i < markers.length; i++){
    let marker = markers[i]

    if(marker){
      if(bounds.contains(marker.getPosition()) && zoom > 5){
        marker.setMap(map)
      } else {
        marker.setMap(null)
      }
    }
  }
}

function openWindow(){
  marker = this
  document.getElementById("title").innerHTML = marker.title;
  document.getElementById('address').innerHTML = marker.address;
  document.getElementById('link').innerHTML = marker.link;

  infoWindow.open(map,marker)
}

function addresses_to_markers() {
  let data = httpGet('/addresses')
  addresses = JSON.parse(data)
  keys = Object.keys(addresses)

  geocoder = new google.maps.Geocoder();

  for(var i = 0; i<keys.length; i++){
    let address = addresses[keys[i]]
    let name = keys[i]

    geocoder.geocode( { 'address': address }, (results, status) =>{
    if (status == google.maps.GeocoderStatus.OK) {
      let place = results[0]
      markers.push(createMarker(place,name,address))
    } else {
      alert('Geocode was not successful for the following reason: ' + status)
    }
    });
  }
}

function createMarker(place,name,address) {
  let marker = new google.maps.Marker({
    map: null,
    position: place.geometry.location,
    animation: google.maps.Animation.DROP,
    label:name[0],

    title:name,
    link:'http://link.com',
    address:address,

  });
  google.maps.event.addListener(marker, 'click', openWindow);
  return marker

  // google.maps.event.addListener(marker, 'click', function() {
  //   infowindow.setContent(place.name);
  //   infowindow.open(map, this);
  // });
}

// function addResult(result, i) {
//         var results = document.getElementById('results');

//         var tr = document.createElement('tr');

//         tr.onclick = function() {
//           google.maps.event.trigger(markers[i], 'click');
//         };

//         var nameTd = document.createElement('td');
//         var name = document.createTextNode(result.name);
//         nameTd.appendChild(name);
//         tr.appendChild(nameTd);
//         results.appendChild(tr);
//       }
// $(document).ready(function () {
// google.maps.event.addDomListener(window, 'load', initMap);
// });
