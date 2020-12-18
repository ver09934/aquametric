$(document).ready(function(){

    var stageMarker = L.icon({
        iconUrl: '/static/images/stageMarker.png',
        iconSize:     [28.8, 45], // size of the icon
        iconAnchor:   [16, 50],   // point of the icon which will correspond to marker's location
        popupAnchor:  [16, -50]   // point from which the popup should open relative to the iconAnchor
    });

    var mymap = L.map('map').setView([42.784723, -73.842862], 9);
    var group = L.layerGroup()
    /*
    var Hydda_Full = L.tileLayer('https://{s}.tile.openstreetmap.se/hydda/full/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mymap);
    */
    var CartoDB_Positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 19
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
                
                $("#stage-graph").attr("src", "/data/"+sensorID+"/plot.png?field=stage&hours=168");
                $("#temp-graph").attr("src", "/data/"+sensorID+"/plot.png?field=temp&hours=168");
                $("#cond-graph").attr("src", "/data/"+sensorID+"/plot.png?field=conductivity&hours=168");
                
                $.ajax({url: "/data/" + sensorID + "/log.json?latest"}).done(function(logData) {
                    
                    console.log("Current data:");
                    console.log(logData);
                    var date = new Date(logData["published_at"]);
                    $("#last-seen").html(" · last connected " + timeago(Date.now() - date.getTime()));

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

function timeago(ms) {

  var ago = Math.floor(ms / 1000);
  var part = 0;

  if (ago < 60) { return "seconds ago"; }

  if (ago < 120) { return "a minute ago"; }
  if (ago < 3600) {
    while (ago >= 60) { ago -= 60; part += 1; }
    return part + " minutes ago";
  }

  if (ago < 7200) { return "an hour ago"; }
  if (ago < 86400) {
    while (ago >= 3600) { ago -= 3600; part += 1; }
    return part + " hours ago";
  }

  if (ago < 172800) { return "a day ago"; }
  if (ago < 604800) {
    while (ago >= 172800) { ago -= 172800; part += 1; }
    return part + " days ago";
  }

  if (ago < 1209600) { return "a week ago"; }
  if (ago < 2592000) {
    while (ago >= 604800) { ago -= 604800; part += 1; }
    return part + " weeks ago";
  }

  if (ago < 5184000) { return "a month ago"; }
  if (ago < 31536000) {
    while (ago >= 2592000) { ago -= 2592000; part += 1; }
    return part + " months ago";
  }

  if (ago < 1419120000) { // 45 years, approximately the epoch
    return "more than year ago";
  }

  // TODO pass in Date.now() and ms to check for 0 as never
  return "never";
}
