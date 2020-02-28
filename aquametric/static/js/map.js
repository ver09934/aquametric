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

    $.ajax({url: "/sensors.json"}).done(function(data) {

        for (var id of Object.keys(data)) {
            sensorInfo = data[id]
            var location = L.latLng(sensorInfo["lat"], sensorInfo["lng"]);
            var marker = L.marker(location, {icon: stageMarker});
            marker.on('click', wrapper(id));
            marker.addTo(mymap);
        }

        function wrapper(sensorID) { 
            return function(clickData) {
                
                console.log("Sensor ID: " + sensorID);
                console.log("Click data:");
                console.log(clickData);

                document.getElementById("flash").style.display = "block";
                $("#flash").fadeIn(350);

                document.getElementById('photo').src = data[sensorID]["img"];
                document.getElementById("title").innerHTML = data[sensorID]["prettyname"];
                document.getElementById("idnum").innerHTML = "#" + sensorID;

                $(".unfocused").removeClass('unfocused');
                $("#sensorlink a").attr("href", "/sensor/" + sensorID);

                $("#flash").fadeOut(350);
            };
        }

    });
});
