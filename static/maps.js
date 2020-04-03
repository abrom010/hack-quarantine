var map;
var service;
var infowindow;
var geocoder;
var autocomplete;
var markers = [];

// const sleep = (milliseconds) => {
//   return new Promise(resolve => setTimeout(resolve, milliseconds))
// }

function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
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
          marker = markers[i]
          console.log(marker)
          if(marker){
            if(bounds.contains(marker.getPosition()) && zoom > 5){
              marker.setMap(map)
              console.log("map set!")
            } else {
              marker.setMap(null)
              console.log("not work :(")
            }
          } else { console.log("not marker D:")};
        }

        
      }

// function clearMarkers() {
//         for (var i = 0; i < markers.length; i++) {
//           if (markers[i]) {
//             markers[i].setMap(null);
//           }
//         }
//         markers = [];
//       }

function addresses_to_markers() {
  let data = httpGet('/addresses')
  addresses = JSON.parse(data)
  geocoder = new google.maps.Geocoder();

  for(var i = 0; i < addresses.length; i++){
    var address = addresses[i]
    console.log(address)
    // sleep(5000).then(() => {
      geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        let place = results[0]
        markers.push(createMarker(place))
      } else {
        alert('Geocode was not successful for the following reason: ' + status)
      }
      });
    // })
  }
}

function createMarker(place) {
  return new google.maps.Marker({
    map: null,
    position: place.geometry.location,
    animation: google.maps.Animation.DROP
  });

  // google.maps.event.addListener(marker, 'click', function() {
  //   infowindow.setContent(place.name);
  //   infowindow.open(map, this);
  // });
}
