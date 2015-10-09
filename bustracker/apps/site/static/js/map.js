/*
    This module takes control of how to create an Map and how to add and control a Bus on it.
    You may want to take a look at: https://developers.google.com/maps/documentation/javascript/tutorial
*/

var map = function (module) {
    /*
        Init the Map.
        Call this before everything.
    */
    module.init = function (busImgPath, initialLatitude, initialLongitude, userLocation) {
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            center: {
                lat: initialLatitude,
                lng: initialLongitude
            }
        });

        if (userLocation) {
            var marker = new google.maps.Marker({
                position: {
                    lat: initialLatitude,
                    lng: initialLongitude
                },
                animation: google.maps.Animation.DROP,
                map: map,
                title: 'Você'
            });
        }

        var trafficLayer = new google.maps.TrafficLayer();
        trafficLayer.setMap(map);

        var transitLayer = new google.maps.TransitLayer();
        transitLayer.setMap(map);

        module._map = map;
        module._busImgPath = busImgPath;
        module._busList = {};
    };

    /*
        Place a Bus on the Map.
    */
    module.addBus = function (id, description, latitude, longitude) {
        var marker = new google.maps.Marker({
            position: {
                lat: latitude,
                lng: longitude
            },
            map: module._map,
            icon: module._busImgPath,
            title: description
        });

        // TODO:
        var contentString = '<div class="bus-info">' +
                            '    <h2>' + description + '</h2>' +
                            '    <label>Terminal</label><span>2-TERMINAL FONTE</span><br>' +
                            '    <label>Linha</label><span>11 - TRONCAL - VIA 2 DE SETEMBRO</span><br>' +
                            '    <label>Sentido</label><span>Terminal Aterro/ Terminal Fonte</span><br>' +
                            '    <label class="last">Última atualização</label><span>20:30</span><br>' +
                            '</div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString,
        });

        marker.addListener('click', function() {
            console.log(arguments);
            infowindow.open(module._map, marker);
        });

        module._busList[id] = marker;
    };

    /*
        Remove a Bus from the Map.
    */
    module.removeBus = function (id) {
        var bus = module._busList[id];

        if (bus) {
            bus.setMap(null);
            delete module._busList[id];
        }
    };

    /*
        Update Bus location on Map.
    */
    module.updateBusLocation = function (id, latitude, longitude) {
        var bus = module._busList[id];

        if (bus) {
            bus.setPosition({
                lat: latitude,
                lng: longitude
            });
        }
    };

    return module;
}({});