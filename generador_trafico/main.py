import os
import requests
import time
from pymongo import MongoClient
from random import gauss, choice

mongoClient = MongoClient(
    host="mongodb",
    port=27017,
    username="admin",
    password="password",
    authSource="admin",
    authMechanism='SCRAM-SHA-256'
)

def get_events_db():
    db = mongoClient.admin
    events_collection = db.waze_events
    return list(events_collection.find({}))

def get_events_random(m=10000):
    events = get_events_db()
    result = list(events)

    while len(result) < m:
        result.append(choice(events))

    return result

# nota: este "m" es el largo final de la lista con los eventos duplicados NO la cantidad de eventos individuales
def get_events_normal(m=10000): 
    events = get_events_db()
    n = len(events)
    mean = n / 2
    stddev = n / 6

    weighted_events = []

    while len(weighted_events) < m:
        # Genera un índice con distribución normal y lo redondea al más cercano válido
        idx = int(gauss(mean, stddev))
        idx = max(0, min(n - 1, idx))  # Evita salir del rango
        weighted_events.append(events[idx])

    return weighted_events

def make_requests_events(events):
    for event in events:
        event.pop("_id", None)
        try:
            requests.post("http://cachechito:9090", json=event)
        except:
            pass

def main():
    modo = os.getenv("MODO_DISTRIBUCION", "aleatorio")
    print(f"GENERADOR DE TRÁFICO - DISTRIBUCIÓN: {modo}")
    mul = int(os.getenv("MULTIPLICADOR", "1"))

    if len(get_events_db()) == 0:
        return

    for i in range(mul, 0, -1):
        if modo == "normal":
            eventos = get_events_normal()
        else:
            eventos = get_events_random()
        
        make_requests_events(eventos)

if __name__ == "__main__":

    time.sleep(5)
    main()
