// FUNÇÃO PARA DESENHAR O MAPA E O CAMINHO
function drawPath(pathData) {
    // VERIFICA SE VARIÁVEL pathData POSSUI VALOR
    if (!pathData || pathData.length === 0) {
        console.error("Error: No route data found.");
        return;
    }

    // ARMAZENA VÉRTICE DE DESTINO
    targetNode = pathData.target

    // ARMAZENA VÉRTICES DO CAMINHO MENOS CUSTOSO
    path = pathData.path

    // CONVERTE COORDENADAS DOS PONTOS PARA FORMATO DE MAPA
    var routeCoords = path.map(point => [point.lon, point.lat]);
    var transformedRouteCoords = routeCoords.map(coord => ol.proj.fromLonLat(coord));

    // CRIA UMA FEATURE (RECURSO) OPENLAYERS PARA REPRESENTAR A ROTA NO MAPA
    var routeFeature = new ol.Feature({
        geometry: new ol.geom.LineString(transformedRouteCoords)
    });

    // DEFINE ESTILO DA LINHA DA ROTA
    routeFeature.setStyle(new ol.style.Style({
        stroke: new ol.style.Stroke({ color: 'red', width: 10 })
    }));

    // INICIALIZA FONTES E CAMADAS PARA O MAPA
    var vectorSource = new ol.source.Vector();
    var vectorLayer = new ol.layer.Vector({ source: vectorSource });

    // CRIA O MAPA E DEFINE SUA VISUALIZAÇÃO
    var map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({ source: new ol.source.OSM() }),
            vectorLayer
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat(routeCoords[0]), // CENTRALIZA NO PONTO INICIAL
            zoom: 20
        })
    });

    // CRIA E ADICIONA MARCADORES PARA PONTOS DE INÍCIO E DESTINO
    var startMarker = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(routeCoords[0]))
    });
    var endMarker = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(routeCoords[routeCoords.length - 1]))
    });

    // DEFINE ESTILO PARA O MARCADOR DO PONTO INICIAL
    startMarker.setStyle(new ol.style.Style({
        image: new ol.style.Circle({
            radius: 7,
            fill: new ol.style.Fill({ color: 'green' }),
            stroke: new ol.style.Stroke({ color: 'green', width: 10 })
        })
    }));

    // DEFINE ESTILO PARA O MARCADOR DO DESTINO (INCLUI ÍCONE E TEXTO)
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

    // ADICIONA OS MARCADORES E A ROTA AO MAPA
    vectorSource.addFeatures([routeFeature, startMarker, endMarker]);

    // CRIA UM MARCADOR PARA RASTREAMENTO 
    var locationFeature = new ol.Feature({
        geometry: new ol.geom.Point(ol.proj.fromLonLat(routeCoords[0])) // POSIÇÃO INICIAL (TEMPORÁRIA)
    });

    // DEFINE ESTILO DO MARCADOR DE LOCALIZAÇÃO ATUAL
    locationFeature.setStyle(new ol.style.Style({
        image: new ol.style.Icon({
            scale: 0.2, // AJUSTA O TAMANHO DO ÍCONE
            src: '../resources/profile.png' // IMAGEM PERSONALIZADA PARA O ÍCONE DE LOCALIZAÇÃO
        })
    }));

    // ADICIONA MARCADOR DE LOCALIZAÇÃO AO MAPA
    vectorSource.addFeature(locationFeature);
}