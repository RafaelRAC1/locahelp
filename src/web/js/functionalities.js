url = 

fakeCoordinates = [-23.545126, -46.240049]

alertButton = document.getElementById("alert-button")

alertButton.addEventListener("click", async () => {
    try {
        const path = await fetchPath(`http://127.0.0.1:8000/shortest-path/?start=-23.545126&start=-46.240049`);
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
