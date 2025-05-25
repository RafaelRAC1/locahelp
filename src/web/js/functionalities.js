// DELIMITA AS COORDENADAS PRÉ-DEFINIDAS DO WEBSITE
fakeCoordinates = [[-23.51470, -46.18542, 'Sul da UBC', 'https://i.ibb.co/632wq08/SUL-UBC.png'], [-23.51535, -46.18326, 'Norte da UMC', 'https://i.ibb.co/21MzSXc3/NORTE-UMC.png'], [-23.518224, -46.181371, 'Sul UMC', 'https://i.ibb.co/8nB1X5yK/SUL-UMC.png'], [-23.516140, -46.180955, "Shopping Mogi", 'https://i.ibb.co/nM4qfnPq/SHOPPING-MOGI.png']]
active = fakeCoordinates[0]
order = 0

// FUNÇÃO PARA TORNAR PRÓXIMA COORDERNADA COMO ATIVA
function alternateCoords() {
    switch (order) {
        case 0:
            active = fakeCoordinates[1]
            order = order + 1
            break
        case 1:
            active = fakeCoordinates[2]
            order = order + 1
            break
        case 2:
            active = fakeCoordinates[3]
            order = order + 1
            break
        case 3:
            active = fakeCoordinates[0]
            order = 0
            break
    }
}

// OBTEM BOTAO PARA ABRIR TELA DE CAMINHOS PREDEFINIDOS
localationsButton = document.getElementById("locations-button")
// OBTEM CONTAINER DE CAMINHO PREDEFINIDOS
locs = document.getElementById("locs")

// ADICIONA OS CAMINHOS PREDEFINIDOS NO CONTAINER DE CAMINHOS
iteration = 0
fakeCoordinates.forEach(fakeCoords => {
    const locationDiv = document.createElement('div')
    locationDiv.classList.add('location')
    const locationImg = document.createElement('img')
    locationImg.src = fakeCoords[3]
    const locationSpan = document.createElement('span')
    locationSpan.classList.add('location-name')
    locationSpan.innerText = fakeCoords[2]
    locationDiv.appendChild(locationImg)
    locationDiv.appendChild(locationSpan)
    locationDiv.id = iteration
    locationDiv.addEventListener('click', () => {
        locationDiv.id != 3 ? order = locationDiv.id : order = 0
        active = fakeCoordinates[locationDiv.id]
        loadMap()
        locs.classList.add('hide');
    })
    locs.children[0].children[1].appendChild(locationDiv)
    iteration++
});

// LOGICA PARA EXIBIR OU OCULTA CONTAINER DE CAMINHOS
localationsButton.addEventListener('click', () => {
    if (locs.classList.contains('hide')) {
        locs.classList.remove(...['hide']);
        locs.classList.add("animate-locations")
    } else {
        locs.classList.add('hide');
        locs.classList.remove("animate-locations")
    }
});

// OBTEM DIV CONTAINER DAS NOTIFICAÇÕES
notifications = document.getElementById('nots')

// FUNÇÃO PARA REMOVER NOTIFICAÇÃO DA TELA
function removeNotification(element) {
    element.parentNode.classList.add("remove-not")
    setTimeout(() => {
        element.parentNode.remove()
    }, 700)
}

// OBTEM BOTÃO DE PRÓXIMO CAMINHO E ADIONA EVENTO PARA PASSAR PARA NOVO CAMINHO E NOTIFICAR
swapCoordinatesButton = document.getElementById('swap')
swapCoordinatesButton.addEventListener('click', () => {
    alternateCoords()
    nots.innerHTML =
        `
    <div class="not-module">
            <span class="not-title">
                <i class="fa fa-bell" id="not-icon" aria-hidden="true"></i>
                Nova localização! 
            </span>
            <p class="not-body">📍 ${active[2]}</p>
            <button class="not-close" onclick="removeNotification(this)">
                <i class="fa fa-times" aria-hidden="true"></i>
            </button>
        </div>
    `
})


// OBTEM BOTAO PARA ENCONTRAR CAMINHO MENOS CUSTOSO
alertButton = document.getElementById("alert-button")

// OBTEM A DIV PARA DESENHAR O MAPA
map = document.getElementById('map')

// FUNÇÃO ASSINCRONA PARA CONSUMIR API E RETORNAR CAMINHO MAIS CURTO
async function fetchPath(url) {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error('Error in locate path request');
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.log("There was an error!")
        throw error
    }
}

// FUNCAO ASSINCRONA PARA CARREGAR O MAPA COM RESULTADO DA API
async function loadMap() {
    try {
        const path = await fetchPath(`http://127.0.0.1:8000/shortest-path/?start=${active[0]}&start=${active[1]}`);
        map.innerHTML = "";
        drawPath(path.dijkstra);
    } catch (error) {
        console.log("There was an error");
        throw error;
    }
}

// ASSOCIA O CARREGAMENTO DO MAPA À AÇÃO DE CLICAR NO BOTÃO DE ALERTA
alertButton.addEventListener("click", async () => {
    loadMap()
})