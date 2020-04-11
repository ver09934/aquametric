$(document).ready(function(){

    var stageMarker = L.icon({
        iconUrl: '/static/images/stageMarker.png',
        iconSize:     [28.8, 45], // size of the icon
        iconAnchor:   [16, 50],   // point of the icon which will correspond to marker's location
        popupAnchor:  [16, -50]   // point from which the popup should open relative to the iconAnchor
    });

    var mymap = L.map('map').setView([42.784723, -73.842862], 9);
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

                $("#info").fadeOut(0);

                $("#photo").attr("src", data[sensorID]["img"]);
                $("#title").html(data[sensorID]["prettyname"]);
                $("#idnum").html("#" + sensorID);

                $(".unfocused").removeClass('unfocused');
                $("#sensorlink a").attr("href", "/sensor/" + sensorID + "?hours=168");
                
                $.ajax({url: "/data/" + sensorID + "/log.json?latest"}).done(function(logData) {
                    
                    console.log("Current data:");
                    console.log(logData);

                    // fields = ["stage", "temp", "turbidity", "conductivity"];
                    fields = ["stage", "temp", "conductivity"];

                    for (var field of Object.keys(logData["data"])) {
                        if (fields.includes(field)) {
                            console.log("Setting " + field + "...");
                            $("#datatable #" + field + " .number").html(logData["data"][field].toFixed(1));
                        }
                    }

                });
                
                $("#info").fadeIn(700);
            };
        }

    });
});
