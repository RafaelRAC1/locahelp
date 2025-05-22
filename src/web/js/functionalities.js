fakeCoordinates = [[-23.51470, -46.18542, 'Sul da UBC'], [-23.51535, -46.18326, 'Oeste da UMC'], [-23.519161, -46.187288, 'INSS'], [-23.516140, -46.180955, "Shopping Mogi"]]
active = fakeCoordinates[0]
order = 0

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

notifications = document.getElementById('nots')

function removeNotification(element) {
    element.parentNode.classList.add("remove-not")
    setTimeout(() => {
        element.parentNode.remove()
    }, 700)
}

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


alertButton = document.getElementById("alert-button")
map = document.getElementById('map')

alertButton.addEventListener("click", async () => {
    try {
        const path = await fetchPath(`http://127.0.0.1:8000/shortest-path/?start=${active[0]}&start=${active[1]}`);
        map.innerHTML = "";
        drawPath(path.dijkstra);
    } catch (error) {
        console.log("There was an error");
        throw error;
    }
})

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

/*
function getCoordiantes() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                console.log(`Latitude: ${latitude}, Longitude: ${longitude}`);
            },
            (error) => {
                console.error("Error getting location:", error.message);
            }
        );
    } else {
        console.error("Geolocation is not supported by this browser.");
    }
}
*/
