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
        module._busStationImgPath = options.busStationImgPath;
        module._busStopImgPath = options.busStopImgPath;
        module._busGarageImgPath = options.busGarageImgPath;

        module._busList = {};
    };

    /*
        Place a Bus on the Map.
    */
    module.addBus = function (data) {
        var description = data.route.code + ' - ' + data.route.name;
        var marker = new google.maps.Marker({
            position: {
                lat: data.latitude,
                lng: data.longitude
            },
            map: module._map,
            icon: module._busImgPath,
            title: description
        });

        var contentString = '<div class="bus-info">' +
                            '    <h2>' + description + '</h2>' +
                            '    <label>Número</label><span>' + data.route.code + '</span><br>' +
                            '    <label>Linha</label><span>' + data.route.name + '</span><br>' +
                            '    <label>Terminal</label><span>' + data.route.from.name + ' / ' + data.route.to.name + '</span><br>' +
                            '    <a href="/bus-route?id=' + data.id + '">Mais Detalhes</a>' +
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
        var icon;

        if (data.type === 'garage') {
            icon = module._busGarageImgPath;
        } else if (data.type === 'bus-stop') {
            icon = module._busStopImgPath;
        } else {
            icon = module._busStationImgPath;
        }

        var marker = new google.maps.Marker({
            position: {
                lat: data.latitude,
                lng: data.longitude
            },
            map: module._map,
            icon: icon,
            title: data.name
        });

        var contentString = '<div class="bus-info">' +
                            '    <h2>' + data.name + '</h2>' +
                            '    <p>' + data.details + '</p>' +
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
                lat: data.latitude,
                lng: data.longitude
            });
        }
    };

    return module;
}({});