$(document).ready(function(){

    var stageMarker = L.icon({
        iconUrl: '/static/images/stageMarker.png',
        iconSize:     [28.8, 45], // size of the icon
        iconAnchor:   [16, 50],   // point of the icon which will correspond to marker's location
        popupAnchor:  [16, -50]   // point from which the popup should open relative to the iconAnchor
    });

    var mymap = L.map('map').setView([42.784723, -73.842862], 8);
    var group = L.layerGroup()

    var Hydda_Full = L.tileLayer('https://{s}.tile.openstreetmap.se/hydda/full/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mymap);

    $.ajax({
        url: "/sensors.json"
    }).done(function(data) {
        
        for (var id of Object.keys(data)) {
            sensorInfo = data[id]
            var location = L.latLng(sensorInfo["lat"], sensorInfo["lng"]);
            var marker = L.marker(location, {icon: stageMarker});
            marker.on('click', wrapper(id));
            marker.addTo(mymap);
        }

        // e is the marker index
        // val is the click data from leaflet
        function wrapper(e){ 
            return function(val) {
                console.log(val);
                console.log(e);
                markerOnClick();
            };
        }
        
        function markerOnClick() {
            document.getElementById("flash").style.display = "block";
            $("#flash").fadeIn(350);
            $("#flash").fadeOut(350);
        }

    });

    /*
    var locations = [
        L.latLng(42.784723, -73.842862),
        L.latLng(43.1, -74.1)
    ];

    for (var i = 0; i < locations.length; i++) {
        var marker = L.marker(locations[i], {icon: stageMarker});
        marker.on('click', wrapper(i));
        marker.addTo(mymap);
    }
    */

});
