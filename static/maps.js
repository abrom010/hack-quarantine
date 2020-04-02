// This example requires the Places library. Include the libraries=places
// parameter when you first load the API. For example:
// <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&libraries=places">

var map;
var service;
var infowindow;
var geocoder;

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds))
}

function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.response;
  }

function initMap() {
  console.log('INIT')
  var latlong = new google.maps.LatLng(-33.867, 151.195); //sydney
  var mapOptions = {
      zoom: 8,
      center: latlong,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }

  infowindow = new google.maps.InfoWindow();

  map = new google.maps.Map(
      document.getElementById('map'), mapOptions);
  codeAddress();

  // var request = {
  //   query: 'Museum of Contemporary Art Australia',
  //   fields: ['name', 'geometry'],
  // };


  // service = new google.maps.places.PlacesService(map);

  // service.findPlaceFromQuery(request, function(results, status) {
  //   if (status === google.maps.places.PlacesServiceStatus.OK) {
  //     for (var i = 0; i < results.length; i++) {
  //       createMarker(results[i]);
  //     }

  //     map.setCenter(results[0].geometry.location);
  //   }
  // });
}

function codeAddress() {
  let addresses = httpGet('/addresses')
  geocoder = new google.maps.Geocoder();
  address = addresses[0] //this is doing [
  console.log(address) // addresses is a string not a list

  geocoder.geocode( { 'address': address}, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      let place = results[0]
      createMarker(place)

    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });

  // for(var i = 0; i < addresses.length; i++){
  //   var address = addresses[i]
  // // var address = "1600 Amphitheatre Parkway, Mountain View, CA" //document.getElementById('address').value;
  //   sleep(10000).then(() => {
  //     geocoder.geocode( { 'address': address}, function(results, status) {
  //     if (status == google.maps.GeocoderStatus.OK) {
  //       let place = results[0]
  //       //map.setCenter(place.geometry.location);
  //       createMarker(place)

  //     } else {
  //       alert('Geocode was not successful for the following reason: ' + status);
  //     }
  //     });
  //   })
  // }
}

function createMarker(place) {
  var marker = new google.maps.Marker({
    map: map,
    position: place.geometry.location
  });

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent(place.name);
    infowindow.open(map, this);
  });
}
