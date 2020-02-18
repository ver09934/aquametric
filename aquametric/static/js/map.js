$(document).ready(function(){

var stageMarker = L.icon({
    iconUrl: 'images/stageMarker.png',

    iconSize:     [28.8, 45], // size of the icon
    iconAnchor:   [16, 50], // point of the icon which will correspond to marker's location
    popupAnchor:  [16, -50] // point from which the popup should open relative to the iconAnchor
});

var mymap = L.map('map').setView([42.784723, -73.842862], 8);
var group = L.layerGroup()
var info;

var Hydda_Full = L.tileLayer('https://{s}.tile.openstreetmap.se/hydda/full/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: 'Tiles courtesy of <a href="http://openstreetmap.se/" target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(mymap);

var locations = [
    L.latLng(42.784723, -73.842862),

];
var i;
var id = 0;
for(i = 0; i < locations.length; i++) {
    var marker = L.marker(locations[i], {icon: stageMarker}).on('click',markerOnClick).addTo(mymap);
}
    
function markerOnClick(e) {
    document.getElementById("flash").style.display = "block";
    $("#flash").fadeIn(350);
    $("#flash").fadeOut(350);
}
});