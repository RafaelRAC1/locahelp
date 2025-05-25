from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from algorithms.dijsktra import shortest_path

# INICIALIZA FASTAPI
app = FastAPI()

# DELIMITA OS INTERMÉDIOS E PARÂMETROS ACEITOS PARA COMUNICAÇÃO
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# DELIMITA ENDPOINT GET PARA RETORNAR O CAMINHO MAIS CURTO, PASSANDO CORDENADAS DE INÍCIO
@app.get("/shortest-path")
def dijkstra(start: List[float] = Query(...)):
    path = shortest_path(start)
    return {"dijkstra": path}