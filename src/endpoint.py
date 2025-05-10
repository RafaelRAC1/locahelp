from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from main import shortest_path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get("/shortest-path")
def dijkstra(start: List[float] = Query(...)):
    """
    API Endpoint to find the shortest path in a road network.
    Example request: /shortest-path?bbox=[37.77,37.78,-122.42,-122.41]&source=123&target=456
    """
    path = shortest_path(start)
    return {"dijkstra": path}