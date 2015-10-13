/*
    This module takes control of how to create an Map and how to add and control a Bus on it.
    You may want to take a look at: https://developers.google.com/maps/documentation/javascript/tutorial
*/

var map = function (module) {
    /*
        Init the Map.
        Call this before everything.
    */
    module.init = function (options) {
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            center: {
                lat: options.initialLatitude,
                lng: options.initialLongitude
            }
        });

        if (options.isUserLocation) {
            var marker = new google.maps.Marker({
                position: {
                    lat: options.initialLatitude,
                    lng: options.initialLongitude
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
        module._busImgPath = options.busImgPath;
        module._busTerminalImgPath = options.busTerminalImgPath;
        module._busList = {};
    };

    /*
        Place a Bus on the Map.
    */
    module.addBus = function (data) {
        var description = data.bus_code + ' - ' + data.route_name;
        var marker = new google.maps.Marker({
            position: {
                lat: data.gps_data.latitude,
                lng: data.gps_data.longitude
            },
            map: module._map,
            icon: module._busImgPath,
            title: description
        });

        var contentString = '<div class="bus-info">' +
                            '    <h2>' + description + '</h2>' +
                            '    <label>Linha</label><span>' + data.route_name + '</span><br>' +
                            '    <label>Terminal</label><span>' + data.from_terminal + ' / ' + data.to_terminal + '</span><br>' +
                            '    <label>Velocidade média</label><span>' + data.gps_data.velocity + ' km/H</span><br>' +
                            '    <label class="last">Última atualização</label><span>' + data.gps_data.last_update + '</span><br>' +
                            '</div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString,
        });

        marker.addListener('click', function() {
            infowindow.open(module._map, marker);
        });

        module._busList[data.device_id] = marker;
    };

    /*
        Place a Terminal on the Map.
    */
    module.addTerminal = function (data) {
        var marker = new google.maps.Marker({
            position: {
                lat: data.latitude,
                lng: data.longitude
            },
            map: module._map,
            icon: module._busTerminalImgPath,
            title: data.name
        });

        var contentString = '<div class="bus-info">' +
                            '    <h2>' + data.name + '</h2>' +
                            '</div>';

        var infowindow = new google.maps.InfoWindow({
            content: contentString,
        });

        marker.addListener('click', function() {
            infowindow.open(module._map, marker);
        });
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
    module.updateBusLocation = function (data) {
        var bus = module._busList[data.device_id];

        if (bus) {
            bus.setPosition({
                lat: data.gps_data.latitude,
                lng: data.gps_data.longitude
            });
        }
    };

    return module;
}({});