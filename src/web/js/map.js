function drawPath(pathData) {
    if (!pathData || pathData.length === 0) {
        console.error("Error: No route data found.");
        return;
    }

    targetNode = pathData.target
    path = pathData.path

    var routeCoords = path.map(point => [point.lon, point.lat]);
    var transformedRouteCoords = routeCoords.map(coord => ol.proj.fromLonLat(coord));

    var routeFeature = new ol.Feature({
        geometry: new ol.geom.LineString(transformedRouteCoords)
    });

    routeFeature.setStyle(new ol.style.Style({
        stroke: new ol.style.Stroke({ color: 'red', width: 10 })
    }));

    var vectorSource = new ol.source.Vector();
    var vectorLayer = new ol.layer.Vector({ source: vectorSource });

    var map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({ source: new ol.source.OSM() }),
            vectorLayer
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat(routeCoords[0]), // Center on start point
            zoom: 20
        })
    });

    // Create and add markers for start and end points
    var startMarker = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(routeCoords[0]))
    });

    var endMarker = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(routeCoords[routeCoords.length - 1]))
    });

    startMarker.setStyle(new ol.style.Style({
        image: new ol.style.Circle({
            radius: 7,
            fill: new ol.style.Fill({ color: 'green' }),
            stroke: new ol.style.Stroke({ color: 'green', width: 10 })
        })
    }));

    endMarker.setStyle(new ol.style.Style({
        image: new ol.style.Icon({
            scale: .4,
            src: `${targetNode.foto}`,
        }),
        text: new ol.style.Text({
        text: targetNode.local || "Destino",
        offsetY: -100,
        font: 'bold 35px sans-serif',
        textAlign: 'center'
    })
    }));

    vectorSource.addFeatures([routeFeature, startMarker, endMarker]);

    // Real-time tracking marker
    var locationFeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(routeCoords[0])) // Start position (temporary)
    });

    locationFeature.setStyle(new ol.style.Style({
        image: new ol.style.Icon({
            scale: 0.2, // Adjust the size of the icon
            src: '../data/profile.png' // Replace with your actual image URL
        })
    }));

    vectorSource.addFeature(locationFeature);

    // Geolocation tracking
    /*
    if (navigator.geolocation) {
        navigator.geolocation.watchPosition(
            function (position) {
                var coords = [position.coords.longitude, position.coords.latitude];
                var transformedCoords = ol.proj.fromLonLat(coords);

                locationFeature.setGeometry(new ol.geom.Point(transformedCoords));
                map.getView().setCenter(transformedCoords);
            },
            function (error) {
                console.error("Geolocation error: ", error);
            },
            { enableHighAccuracy: true }
        );
    } else {
        console.error("Geolocation is not supported.");
    }
    */
}